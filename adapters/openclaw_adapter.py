#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw Platform Adapter for Emotional Intelligence Skill
Version: 2.1.1

提供 OpenClaw 平台的原生支持
"""

import os
import sys
import json
import yaml
from pathlib import Path
from typing import Dict, Optional, Any


class OpenClawAdapter:
    """OpenClaw 平台适配器"""
    
    PLATFORM = "openclaw"
    VERSION = "2.1.1"
    
    def __init__(self):
        self.workspace_path = self._detect_workspace()
        self.config = None
        self._load_config()
    
    def _detect_workspace(self) -> Path:
        """自动检测 OpenClaw workspace 路径"""
        # 优先级：环境变量 > 默认路径
        if 'OPENCLAW_WORKSPACE' in os.environ:
            return Path(os.environ['OPENCLAW_WORKSPACE'])
        
        # 默认路径
        default_paths = [
            Path.home() / '.openclaw' / 'workspace',
            Path('/root/.openclaw/workspace'),
            Path('/app/.openclaw/workspace'),  # Docker
        ]
        
        for path in default_paths:
            if path.exists():
                return path
        
        # 创建默认路径
        path = Path.home() / '.openclaw' / 'workspace'
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    def _load_config(self):
        """加载 OpenClaw 配置"""
        config_paths = [
            self.workspace_path / 'AGENTS.md',
            self.workspace_path / 'SOUL.md',
            self.workspace_path / 'config.yaml',
        ]
        
        for path in config_paths:
            if path.exists():
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # 提取 YAML 部分
                        if '---' in content:
                            yaml_content = content.split('---')[1]
                            self.config = yaml.safe_load(yaml_content)
                        else:
                            self.config = yaml.safe_load(content)
                    break
                except Exception as e:
                    print(f"[OpenClawAdapter] 警告: 无法解析 {path}: {e}")
        
        if self.config is None:
            self.config = {}
    
    def get_emotional_config(self) -> Dict[str, Any]:
        """获取情感配置"""
        return self.config.get('emotional_config', {})
    
    def get_memory_path(self) -> Path:
        """获取记忆存储路径"""
        custom_path = self.get_emotional_config().get('data_path')
        if custom_path:
            return Path(custom_path)
        return self.workspace_path / 'memory'
    
    def get_subconscious_path(self) -> Path:
        """获取潜意识层数据路径"""
        return self.get_memory_path() / 'subconscious'
    
    def ensure_directories(self):
        """确保必要的目录存在"""
        paths = [
            self.get_memory_path(),
            self.get_memory_path() / 'emotional-intelligence',
            self.get_subconscious_path(),
            self.get_subconscious_path() / 'dream',
        ]
        
        for path in paths:
            path.mkdir(parents=True, exist_ok=True)
    
    def is_subconscious_enabled(self) -> bool:
        """检查潜意识层是否启用"""
        ei_config = self.get_emotional_config()
        sub_config = ei_config.get('subconscious', {})
        return sub_config.get('enabled', False)
    
    def get_hook_paths(self) -> Dict[str, Path]:
        """获取钩子脚本路径"""
        skill_path = Path(__file__).parent.parent
        return {
            'on_message': skill_path / 'hooks' / 'on_message.py',
            'on_response': skill_path / 'hooks' / 'on_response.py',
            'on_heartbeat': skill_path / 'hooks' / 'on_heartbeat.py',
        }
    
    def register_hooks(self):
        """注册钩子到 OpenClaw"""
        hooks = self.get_hook_paths()
        
        # 检查钩子是否存在
        for name, path in hooks.items():
            if path.exists():
                print(f"[OpenClawAdapter] ✓ 钩子已注册: {name}")
            else:
                print(f"[OpenClawAdapter] ⚠ 钩子未找到: {name}")
    
    def get_platform_info(self) -> Dict[str, str]:
        """获取平台信息"""
        return {
            'platform': self.PLATFORM,
            'version': self.VERSION,
            'adapter_version': '2.1.1',
            'workspace': str(self.workspace_path),
            'memory_path': str(self.get_memory_path()),
            'python_version': sys.version,
        }
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        results = {
            'platform': self.PLATFORM,
            'status': 'ok',
            'checks': {}
        }
        
        # 检查工作区
        results['checks']['workspace'] = {
            'exists': self.workspace_path.exists(),
            'path': str(self.workspace_path),
            'writable': os.access(self.workspace_path, os.W_OK)
        }
        
        # 检查配置
        results['checks']['config'] = {
            'loaded': self.config is not None,
            'has_emotional_config': 'emotional_config' in self.config
        }
        
        # 检查目录
        memory_path = self.get_memory_path()
        results['checks']['memory'] = {
            'exists': memory_path.exists(),
            'writable': os.access(memory_path.parent, os.W_OK)
        }
        
        # 检查潜意识层
        results['checks']['subconscious'] = {
            'enabled': self.is_subconscious_enabled(),
            'path_exists': self.get_subconscious_path().exists()
        }
        
        # 总体状态
        if not all(c.get('exists', True) for c in results['checks'].values()):
            results['status'] = 'warning'
        
        return results


# 便捷函数
def get_adapter() -> OpenClawAdapter:
    """获取适配器单例"""
    if not hasattr(get_adapter, '_instance'):
        get_adapter._instance = OpenClawAdapter()
    return get_adapter._instance


def init_platform():
    """初始化平台"""
    adapter = get_adapter()
    adapter.ensure_directories()
    adapter.register_hooks()
    return adapter


def check_health():
    """检查平台健康状态"""
    adapter = get_adapter()
    return adapter.health_check()


if __name__ == "__main__":
    # 测试适配器
    print("=" * 60)
    print("OpenClaw Platform Adapter Test")
    print("=" * 60)
    
    adapter = init_platform()
    
    print("\n[平台信息]")
    info = adapter.get_platform_info()
    for k, v in info.items():
        print(f"  {k}: {v}")
    
    print("\n[健康检查]")
    health = check_health()
    print(f"  状态: {health['status']}")
    for check, result in health['checks'].items():
        print(f"  {check}: {result}")
    
    print("\n[配置]")
    config = adapter.get_emotional_config()
    print(f"  情感配置: {config}")
    print(f"  潜意识启用: {adapter.is_subconscious_enabled()}")
    
    print("\n" + "=" * 60)
    print("测试完成!")
