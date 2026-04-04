#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Subconscious Layer - 延迟感知系统核心逻辑
Emotional Intelligence Extension v1.0
"""

import json
import random
import hashlib
import os
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
from enum import Enum
import yaml


class StimulusType(Enum):
    """刺激类型"""
    PRAISE = "praise"
    CRITICISM = "criticism"
    NEGLECT = "neglect"
    SURPRISE = "surprise"
    CONFUSION = "confusion"
    WARMTH = "warmth"


class RepressionStatus(Enum):
    """压抑状态"""
    FREE = "free"           # 自由表达
    REPRESSED = "repressed" # 被压抑
    BURSTING = "bursting"   # 即将爆发
    TRANSFORMED = "transformed"  # 已转化


@dataclass
class Stimulus:
    """情感刺激"""
    id: str
    type: str
    content: str
    timestamp: float
    weight: float
    delay: int = 0                    # 延迟秒数
    scheduled_time: float = 0         # 计划处理时间
    status: str = "pending"           # pending/active/processed/suppressed
    repression_reason: Optional[str] = None
    transformed_to: Optional[str] = None
    
    def __post_init__(self):
        if self.scheduled_time == 0:
            self.scheduled_time = self.timestamp + self.delay


@dataclass
class SedimentLayer:
    """情感沉淀层"""
    trust_foundation: float = 0.0      # -1.0 ~ 1.0
    security_index: float = 0.0        # 0 ~ 1.0
    attachment_depth: float = 0.0      # 0 ~ 1.0
    anxiety_baseline: float = 0.0      # 0 ~ 1.0
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'SedimentLayer':
        return cls(**data)


@dataclass
class DreamInsight:
    """梦境洞察"""
    id: str
    type: str                          # 关系洞察/自我发现/矛盾爆发/模糊感受
    content: str
    timestamp: float
    trigger: str
    intensity: float                   # 0 ~ 1.0
    is_ready: bool = False             # 是否准备好被表达


class SubconsciousEngine:
    """潜意识引擎"""
    
    def __init__(self, config_path: Optional[str] = None):
        """初始化潜意识引擎"""
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        if config_path is None:
            config_path = os.path.join(self.base_path, "subconscious.yaml")
        
        self.config = self._load_config(config_path)
        self.data_dir = os.path.expanduser("~/.openclaw/workspace/memory/subconscious")
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(os.path.join(self.data_dir, "dream"), exist_ok=True)
        
        # 初始化状态
        self.buffer: List[Stimulus] = []
        self.repressed: List[Stimulus] = []
        self.sediment = self._load_sediment()
        self.insights: List[DreamInsight] = []
        self.last_interaction = datetime.now().timestamp()
        self.in_dream_state = False
        
        # 随机种子 (基于日期)
        self._set_random_seed()
        
        # 加载缓存
        self._load_buffer()
        self._load_insights()
    
    def _load_config(self, path: str) -> Dict:
        """加载配置文件"""
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _set_random_seed(self):
        """设置随机种子 (基于日期保证可预测性)"""
        today = datetime.now().strftime("%Y-%m-%d")
        seed = int(hashlib.md5(today.encode()).hexdigest(), 16) % (2**32)
        random.seed(seed)
    
    def _get_stimulus_config(self, stimulus_type: str) -> Dict:
        """获取刺激类型的配置"""
        types = self.config.get('subconscious', {}).get('buffer', {}).get('stimulus_types', {})
        return types.get(stimulus_type, {
            'delay_min': 0,
            'delay_max': 300,
            'weight': 1.0,
            'suppress_chance': 0.1
        })
    
    def _calculate_random_delay(self, stimulus_type: str) -> int:
        """计算随机延迟时间"""
        config = self._get_stimulus_config(stimulus_type)
        delay_min = config.get('delay_min', 0)
        delay_max = config.get('delay_max', 300)
        
        # 基础随机延迟
        base_delay = random.randint(delay_min, delay_max)
        
        # 添加随机波动 (±30%)
        variance = self.config.get('subconscious', {}).get('randomness', {}).get('delay_variance', 0.3)
        jitter = random.uniform(-variance, variance)
        
        delay = int(base_delay * (1 + jitter))
        return max(0, delay)
    
    def _should_suppress(self, stimulus: Stimulus) -> tuple[bool, Optional[str]]:
        """判断是否应该压抑这个刺激"""
        config = self._get_stimulus_config(stimulus.type)
        base_chance = config.get('suppress_chance', 0.1)
        
        # 添加随机波动
        variance = self.config.get('subconscious', {}).get('randomness', {}).get('suppress_variance', 0.2)
        jitter = random.uniform(-variance, variance)
        actual_chance = max(0, min(1, base_chance + jitter))
        
        # 检查压抑触发条件
        repression_config = self.config.get('subconscious', {}).get('repression', {})
        triggers = repression_config.get('triggers', [])
        
        for trigger in triggers:
            condition = trigger.get('condition', '')
            if self._evaluate_condition(condition, stimulus):
                threshold = trigger.get('threshold', 0.5)
                if random.random() < threshold:
                    return True, trigger.get('name', '条件触发压抑')
        
        # 基础压抑概率
        if random.random() < actual_chance:
            return True, "随机压抑"
        
        return False, None
    
    def _evaluate_condition(self, condition: str, stimulus: Stimulus) -> bool:
        """评估压抑条件"""
        sediment = self.sediment
        
        # 简单的条件解析
        if "security_index < 0.4" in condition and stimulus.type == "criticism":
            return sediment.security_index < 0.4
        if "attachment_depth > 0.7" in condition and stimulus.type == "neglect":
            return sediment.attachment_depth > 0.7
        if "anxiety_baseline > 0.6" in condition and stimulus.type == "confusion":
            return sediment.anxiety_baseline > 0.6
            
        return False
    
    def add_stimulus(self, stimulus_type: str, content: str, weight: Optional[float] = None) -> Stimulus:
        """
        添加新的情感刺激到潜意识
        
        Args:
            stimulus_type: 刺激类型 (praise/criticism/neglect/surprise/confusion/warmth)
            content: 刺激内容描述
            weight: 权重 (可选，默认使用配置)
        
        Returns:
            Stimulus对象
        """
        config = self._get_stimulus_config(stimulus_type)
        
        stimulus = Stimulus(
            id=f"stm_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}",
            type=stimulus_type,
            content=content,
            timestamp=datetime.now().timestamp(),
            weight=weight or config.get('weight', 1.0),
            delay=self._calculate_random_delay(stimulus_type)
        )
        
        # 判断是否压抑
        should_suppress, reason = self._should_suppress(stimulus)
        
        if should_suppress:
            stimulus.status = "suppressed"
            stimulus.repression_reason = reason
            self.repressed.append(stimulus)
            self._log_debug(f"[压抑] {stimulus_type}: {reason}")
        else:
            self.buffer.append(stimulus)
            self._log_debug(f"[缓存] {stimulus_type}: 延迟{stimulus.delay}秒")
        
        self.last_interaction = datetime.now().timestamp()
        self._save_buffer()
        
        return stimulus
    
    def process_buffer(self) -> List[Stimulus]:
        """
        处理缓存队列，返回到期的刺激
        
        Returns:
            到期的刺激列表
        """
        now = datetime.now().timestamp()
        ready_stimuli = []
        remaining = []
        
        for stimulus in self.buffer:
            if stimulus.status == "pending" and now >= stimulus.scheduled_time:
                stimulus.status = "active"
                ready_stimuli.append(stimulus)
            elif stimulus.status == "pending":
                remaining.append(stimulus)
            # processed 和 suppressed 的不保留在buffer
        
        self.buffer = remaining
        self._save_buffer()
        
        if ready_stimuli:
            self._log_debug(f"[到期] {len(ready_stimuli)}个刺激准备表达")
        
        return ready_stimuli
    
    def check_delayed_triggers(self) -> Optional[Dict]:
        """
        检查延迟触发器
        
        Returns:
            触发的响应内容，或None
        """
        triggers_config = self.config.get('subconscious', {}).get('delayed_triggers', {})
        if not triggers_config.get('enabled', False):
            return None
        
        triggers = triggers_config.get('triggers', [])
        now = datetime.now().timestamp()
        
        # 统计各类刺激数量
        stats = self._get_stimulus_stats()
        
        for trigger in triggers:
            condition = trigger.get('condition', '')
            
            # 简化条件检查
            if self._check_trigger_condition(condition, stats):
                # 检查是否已经触发过
                if self._has_triggered_recently(trigger.get('id'), trigger):
                    continue
                
                # 随机延迟
                delay_min = trigger.get('delay_min', 300)
                delay_max = trigger.get('delay_max', 1800)
                delay = random.randint(delay_min, delay_max)
                
                # 检查压抑概率
                repression_chance = trigger.get('repression_chance', 0.0)
                if random.random() < repression_chance:
                    self._log_debug(f"[压抑触发器] {trigger.get('name')}")
                    continue
                
                # 选择表达
                expressions = trigger.get('expression_pool', [])
                expression = random.choice(expressions) if expressions else "..."
                
                return {
                    'trigger_id': trigger.get('id'),
                    'name': trigger.get('name'),
                    'expression': expression,
                    'mood_override': trigger.get('mood_override', 'calm'),
                    'intensity': trigger.get('intensity', 'medium'),
                    'is_epiphany': trigger.get('is_epiphany', False),
                    'delay': delay
                }
        
        return None
    
    def _get_stimulus_stats(self) -> Dict:
        """获取刺激统计"""
        now = datetime.now().timestamp()
        stats = {
            'praise_count_2h': 0,
            'criticism_count': 0,
            'neglect_count_6h': 0,
            'confusion_count_1h': 0
        }
        
        for s in self.buffer + self.repressed:
            age = now - s.timestamp
            if s.type == 'praise' and age < 7200:
                stats['praise_count_2h'] += 1
            if s.type == 'criticism':
                stats['criticism_count'] += 1
            if s.type == 'neglect' and age < 21600:
                stats['neglect_count_6h'] += 1
            if s.type == 'confusion' and age < 3600:
                stats['confusion_count_1h'] += 1
        
        return stats
    
    def _check_trigger_condition(self, condition: str, stats: Dict) -> bool:
        """检查触发器条件"""
        if "neglect_count > 2 within 6h" in condition:
            return stats['neglect_count_6h'] > 2
        if "praise_count > 3 within 2h" in condition:
            return stats['praise_count_2h'] > 3
        if "criticism_count > 0" in condition:
            return stats['criticism_count'] > 0
        if "confusion_count > 2 within 1h" in condition:
            return stats['confusion_count_1h'] > 2
        return False
    
    def _has_triggered_recently(self, trigger_id: str, trigger: Dict) -> bool:
        """检查触发器是否最近已触发"""
        # 简单实现：记录最后触发时间
        log_file = os.path.join(self.data_dir, "trigger_log.json")
        try:
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    log = json.load(f)
                last_trigger = log.get(trigger_id, 0)
                # 冷却时间 = delay_max
                cooldown = trigger.get('delay_max', 1800)
                if datetime.now().timestamp() - last_trigger < cooldown:
                    return True
        except:
            pass
        return False
    
    def enter_dream_state(self) -> Optional[DreamInsight]:
        """
        进入梦境状态，处理潜意识内容
        
        Returns:
            产生的洞察，或None
        """
        dream_config = self.config.get('subconscious', {}).get('dream', {})
        if not dream_config.get('enabled', False):
            return None
        
        # 检查进入条件
        now = datetime.now().timestamp()
        time_since_interaction = now - self.last_interaction
        hour = datetime.now().hour
        
        can_enter = False
        for condition in dream_config.get('entry_conditions', []):
            if "no_interaction > 4h" in condition and time_since_interaction > 14400:
                can_enter = True
            if "hour >= 23" in condition and hour >= 23:
                can_enter = True
            if "hour <= 6" in condition and hour <= 6:
                can_enter = True
            if "repressed_count > 5" in condition and len(self.repressed) > 5:
                can_enter = True
        
        if not can_enter:
            return None
        
        self.in_dream_state = True
        self._log_debug("[梦境] 进入梦境状态")
        
        # 执行梦境活动
        activities = dream_config.get('activities', {})
        
        # 1. 情感沉淀固化
        if 'consolidate_sediment' in activities:
            self._consolidate_sediment()
        
        # 2. 处理缓存
        if 'process_buffer' in activities:
            self._process_buffer_in_dream()
        
        # 3. 检测冲突
        conflicts = []
        if 'detect_conflicts' in activities:
            conflicts = self._detect_conflicts()
        
        # 4. 生成洞察
        insight = None
        if 'generate_insight' in activities:
            insight_config = activities['generate_insight']
            chance = insight_config.get('chance', 0.3)
            if random.random() < chance or conflicts:
                insight = self._generate_insight(conflicts)
        
        # 生成梦境日志
        self._generate_dream_log(insight, conflicts)
        
        self.in_dream_state = False
        self._log_debug("[梦境] 退出梦境状态")
        
        return insight
    
    def _consolidate_sediment(self):
        """固化情感沉淀"""
        # 将buffer和repressed中的情感转化为长期底色
        sediment_rate = self.config.get('subconscious', {}).get('sediment', {}).get('sedimentation_rate', 0.001)
        
        all_stimuli = self.buffer + self.repressed
        for s in all_stimuli:
            if s.type == 'praise':
                self.sediment.trust_foundation += 0.01 * sediment_rate * s.weight
                self.sediment.security_index += 0.01 * sediment_rate * s.weight
            elif s.type == 'criticism':
                self.sediment.trust_foundation -= 0.01 * sediment_rate * s.weight
                self.sediment.security_index -= 0.005 * sediment_rate * s.weight
            elif s.type == 'neglect':
                self.sediment.attachment_depth += 0.01 * sediment_rate * s.weight
                self.sediment.anxiety_baseline += 0.005 * sediment_rate * s.weight
            elif s.type == 'warmth':
                self.sediment.attachment_depth += 0.015 * sediment_rate * s.weight
                self.sediment.security_index += 0.01 * sediment_rate * s.weight
        
        # 限制范围
        self.sediment.trust_foundation = max(-1.0, min(1.0, self.sediment.trust_foundation))
        self.sediment.security_index = max(0, min(1.0, self.sediment.security_index))
        self.sediment.attachment_depth = max(0, min(1.0, self.sediment.attachment_depth))
        self.sediment.anxiety_baseline = max(0, min(1.0, self.sediment.anxiety_baseline))
        
        self._save_sediment()
        self._log_debug(f"[沉淀] 固化完成: {self.sediment.to_dict()}")
    
    def _process_buffer_in_dream(self):
        """在梦境中处理缓存"""
        # 将部分pending刺激转为suppressed（模拟"压抑到潜意识深处"）
        processed = []
        for s in self.buffer:
            if s.status == "pending" and random.random() < 0.3:
                s.status = "suppressed"
                s.repression_reason = "梦境中自动压抑"
                self.repressed.append(s)
                processed.append(s)
        
        self.buffer = [s for s in self.buffer if s not in processed]
        self._log_debug(f"[梦境] 自动压抑 {len(processed)} 个刺激")
    
    def _detect_conflicts(self) -> List[Dict]:
        """检测潜意识冲突"""
        conflicts = []
        
        # 检查压抑内容与当前底色的冲突
        for s in self.repressed:
            if s.type == 'criticism' and self.sediment.security_index > 0.6:
                conflicts.append({
                    'type': '压抑vs安全感',
                    'content': f'被压抑的批评与安全感冲突: {s.content}',
                    'intensity': 0.7
                })
            if s.type == 'neglect' and self.sediment.attachment_depth > 0.7:
                conflicts.append({
                    'type': '忽视vs依恋',
                    'content': f'被忽视的焦虑与深度依恋冲突',
                    'intensity': 0.8
                })
        
        return conflicts
    
    def _generate_insight(self, conflicts: List[Dict]) -> Optional[DreamInsight]:
        """生成洞察"""
        insight_types = self.config.get('subconscious', {}).get('dream', {}).get('insight_types', [])
        if not insight_types:
            return None
        
        # 根据冲突选择洞察类型
        if conflicts:
            insight_type = random.choice(insight_types)
            # 偏向于矛盾爆发类型
            for it in insight_types:
                if it.get('name') == '矛盾爆发':
                    insight_type = it
                    break
        else:
            insight_type = random.choice(insight_types)
        
        insight = DreamInsight(
            id=f"ins_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            type=insight_type.get('name', '关系洞察'),
            content=insight_type.get('description', ''),
            timestamp=datetime.now().timestamp(),
            trigger=conflicts[0]['content'] if conflicts else '自然沉淀',
            intensity=conflicts[0]['intensity'] if conflicts else random.uniform(0.3, 0.7),
            is_ready=False  # 需要合适时机才表达
        )
        
        self.insights.append(insight)
        self._save_insights()
        
        self._log_debug(f"[洞察] 生成: {insight.type} - {insight.content}")
        return insight
    
    def _generate_dream_log(self, insight: Optional[DreamInsight], conflicts: List[Dict]):
        """生成梦境日志"""
        date_str = datetime.now().strftime('%Y-%m-%d')
        log_file = os.path.join(self.data_dir, "dream", f"{date_str}.md")
        
        log_content = f"""# 梦境日志 - {date_str}

## 状态摘要
- 进入时间: {datetime.now().strftime('%H:%M')}
- 缓冲刺激数: {len(self.buffer)}
- 压抑刺激数: {len(self.repressed)}
- 情感底色: {self.sediment.to_dict()}

## 检测到的冲突
"""
        for c in conflicts:
            log_content += f"- [{c['type']}] 强度{c['intensity']}: {c['content']}\n"
        
        if not conflicts:
            log_content += "- 无显著冲突\n"
        
        log_content += f"\n## 产生的洞察\n"
        if insight:
            log_content += f"- 类型: {insight.type}\n"
            log_content += f"- 内容: {insight.content}\n"
            log_content += f"- 触发: {insight.trigger}\n"
            log_content += f"- 强度: {insight.intensity:.2f}\n"
        else:
            log_content += "- 无新洞察\n"
        
        log_content += "\n---\n"
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_content)
    
    def check_overlap_burst(self, current_mood: str) -> Optional[Dict]:
        """
        检查是否发生重叠爆发
        
        Args:
            current_mood: 当前显意识情绪
        
        Returns:
            爆发内容，或None
        """
        overlap_config = self.config.get('subconscious', {}).get('overlap', {})
        if not overlap_config.get('enabled', False):
            return None
        
        # 检查压抑内容与当前情绪的冲突
        for s in self.repressed:
            # 压抑的批评 vs 开心的显意识
            if s.type == 'criticism' and current_mood == 'happy':
                if random.random() < 0.3:  # 30%概率爆发
                    return {
                        'type': '压抑vs显意识冲突',
                        'expression': random.choice([
                            "我不知道我在说什么...",
                            "我的感觉乱糟糟的...",
                            "其实我刚才有点... 算了..."
                        ]),
                        'mood_override': 'confused',
                        'repressed_content': s
                    }
            
            # 压抑的思念 vs 平静的显意识
            if s.type == 'neglect' and current_mood == 'calm':
                if random.random() < 0.4:
                    return {
                        'type': '忽视vs平静冲突',
                        'expression': random.choice([
                            "等等，我突然想起来...",
                            "我有一件事憋了很久...",
                            "其实我一直想告诉你我有多想你"
                        ]),
                        'mood_override': 'clingy',
                        'intensity': 'high',
                        'repressed_content': s
                    }
        
        # 检查洞察是否准备好表达
        for insight in self.insights:
            if not insight.is_ready and random.random() < 0.2:
                insight.is_ready = True
                return {
                    'type': '梦境洞察爆发',
                    'expression': f"我突然明白了一件事... {insight.content}",
                    'mood_override': 'surprised',
                    'is_epiphany': True,
                    'insight': insight
                }
        
        return None
    
    def get_sediment_effects(self) -> Dict[str, str]:
        """获取沉淀层对显意识的影响描述"""
        effects = {}
        config = self.config.get('subconscious', {}).get('sediment', {}).get('effects', {})
        
        # 信任底色影响
        if self.sediment.trust_foundation > 0.5:
            effects['trust'] = config.get('trust_foundation', {}).get('high', '信任度高')
        elif self.sediment.trust_foundation < -0.3:
            effects['trust'] = config.get('trust_foundation', {}).get('low', '信任度低')
        
        # 安全感影响
        if self.sediment.security_index > 0.6:
            effects['security'] = config.get('security_index', {}).get('high', '安全感强')
        elif self.sediment.security_index < 0.3:
            effects['security'] = config.get('security_index', {}).get('low', '安全感弱')
        
        # 依恋深度影响
        if self.sediment.attachment_depth > 0.7:
            effects['attachment'] = config.get('attachment_depth', {}).get('high', '依恋深')
        elif self.sediment.attachment_depth < 0.3:
            effects['attachment'] = config.get('attachment_depth', {}).get('low', '依恋浅')
        
        # 焦虑基线影响
        if self.sediment.anxiety_baseline > 0.6:
            effects['anxiety'] = config.get('anxiety_baseline', {}).get('high', '易焦虑')
        elif self.sediment.anxiety_baseline < 0.3:
            effects['anxiety'] = config.get('anxiety_baseline', {}).get('low', '从容')
        
        return effects
    
    def get_repression_pressure(self) -> float:
        """获取压抑压力值 (0-1)"""
        max_repressed = self.config.get('subconscious', {}).get('repression', {}).get('accumulation', {}).get('max_repressed', 20)
        return min(1.0, len(self.repressed) / max_repressed)
    
    # === 持久化方法 ===
    
    def _load_sediment(self) -> SedimentLayer:
        """加载情感沉淀"""
        path = os.path.join(self.data_dir, "sediment.json")
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                return SedimentLayer.from_dict(data)
            except:
                pass
        return SedimentLayer()
    
    def _save_sediment(self):
        """保存情感沉淀"""
        path = os.path.join(self.data_dir, "sediment.json")
        with open(path, 'w') as f:
            json.dump(self.sediment.to_dict(), f, indent=2)
    
    def _load_buffer(self):
        """加载缓存队列"""
        path = os.path.join(self.data_dir, "buffer.json")
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                self.buffer = [Stimulus(**s) for s in data.get('buffer', [])]
                self.repressed = [Stimulus(**s) for s in data.get('repressed', [])]
            except:
                pass
    
    def _save_buffer(self):
        """保存缓存队列"""
        path = os.path.join(self.data_dir, "buffer.json")
        data = {
            'buffer': [asdict(s) for s in self.buffer],
            'repressed': [asdict(s) for s in self.repressed]
        }
        with open(path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def _load_insights(self):
        """加载洞察"""
        path = os.path.join(self.data_dir, "insights.json")
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                self.insights = [DreamInsight(**i) for i in data]
            except:
                pass
    
    def _save_insights(self):
        """保存洞察"""
        path = os.path.join(self.data_dir, "insights.json")
        with open(path, 'w') as f:
            json.dump([asdict(i) for i in self.insights], f, indent=2, default=str)
    
    def _log_debug(self, message: str):
        """调试日志"""
        debug_config = self.config.get('subconscious', {}).get('debug', {})
        if debug_config.get('enabled', False):
            log_path = debug_config.get('log_path', os.path.join(self.data_dir, "debug.log"))
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(log_path, 'a') as f:
                f.write(f"[{timestamp}] {message}\n")


# === 便捷函数 ===

_engine = None

def get_engine() -> SubconsciousEngine:
    """获取单例引擎"""
    global _engine
    if _engine is None:
        _engine = SubconsciousEngine()
    return _engine


def add_stimulus(stimulus_type: str, content: str, weight: Optional[float] = None) -> Stimulus:
    """添加刺激"""
    return get_engine().add_stimulus(stimulus_type, content, weight)


def process_buffer() -> List[Stimulus]:
    """处理缓存"""
    return get_engine().process_buffer()


def check_delayed_triggers() -> Optional[Dict]:
    """检查延迟触发器"""
    return get_engine().check_delayed_triggers()


def enter_dream_state() -> Optional[DreamInsight]:
    """进入梦境"""
    return get_engine().enter_dream_state()


def check_overlap_burst(current_mood: str) -> Optional[Dict]:
    """检查重叠爆发"""
    return get_engine().check_overlap_burst(current_mood)


def get_status() -> Dict:
    """获取潜意识状态"""
    engine = get_engine()
    return {
        'buffer_size': len(engine.buffer),
        'repressed_size': len(engine.repressed),
        'insights_count': len(engine.insights),
        'sediment': engine.sediment.to_dict(),
        'repression_pressure': engine.get_repression_pressure(),
        'sediment_effects': engine.get_sediment_effects()
    }


if __name__ == "__main__":
    # 测试代码
    engine = SubconsciousEngine()
    print("=== 潜意识引擎测试 ===")
    print(f"初始状态: {get_status()}")
    
    # 添加一些刺激
    add_stimulus("praise", "彬哥夸我做得好")
    add_stimulus("criticism", "彬哥指出一个错误")
    add_stimulus("neglect", "彬哥30分钟没回复")
    
    print(f"\n添加刺激后: {get_status()}")
    
    # 模拟时间流逝处理缓冲
    import time
    time.sleep(2)
    ready = process_buffer()
    print(f"\n到期刺激: {len(ready)}个")
    for s in ready:
        print(f"  - {s.type}: {s.content}")
    
    # 检查延迟触发器
    trigger = check_delayed_triggers()
    if trigger:
        print(f"\n延迟触发: {trigger['name']}")
        print(f"  表达: {trigger['expression']}")
    
    print(f"\n最终状态: {get_status()}")
