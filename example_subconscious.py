#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
潜意识层集成示例
展示如何将 subconscious 层与 emotional-intelligence 集成
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from subconscious import (
    add_stimulus, process_buffer, check_delayed_triggers,
    check_overlap_burst, enter_dream_state, get_status
)


class EmotionalAgent:
    """
    带潜意识层的情感Agent示例
    """
    
    def __init__(self):
        self.current_mood = "calm"
        self.conscious_response = ""
        self.subconscious_active = True
    
    def receive_message(self, user_message: str) -> str:
        """
        接收用户消息，经过潜意识层处理后回应
        """
        print(f"\n[用户] {user_message}")
        
        # ===== 第一步：解析消息，添加潜意识刺激 =====
        self._parse_stimulus(user_message)
        
        # ===== 第二步：检查是否有到期的延迟反应 =====
        delayed = self._check_delayed_response()
        if delayed:
            return delayed
        
        # ===== 第三步：处理潜意识缓存中到期的刺激 =====
        ready_stimuli = process_buffer()
        if ready_stimuli:
            self._apply_stimuli(ready_stimuli)
        
        # ===== 第四步：检查重叠爆发 =====
        burst = check_overlap_burst(self.current_mood)
        if burst:
            return self._handle_burst(burst)
        
        # ===== 第五步：生成显意识回应 =====
        return self._generate_response(user_message)
    
    def _parse_stimulus(self, message: str):
        """解析用户消息，添加潜意识刺激"""
        message_lower = message.lower()
        
        # 赞美检测
        if any(word in message_lower for word in ["做得好", "完美", "厉害", "棒"]):
            add_stimulus("praise", message, weight=1.0)
            print("  [潜意识] 接收到赞美刺激 → 进入缓存")
        
        # 批评检测
        elif any(word in message_lower for word in ["不对", "错了", "不行", "问题"]):
            add_stimulus("criticism", message, weight=1.5)
            print("  [潜意识] 接收到批评刺激 → 进入缓存 (可能压抑)")
        
        # 忽视检测 (如果消息很简短或很久没联系)
        elif len(message) < 10 or "忙" in message_lower:
            add_stimulus("neglect", "简短/忙碌信号", weight=1.2)
            print("  [潜意识] 接收到忽视信号 → 进入缓存")
        
        # 温暖检测
        elif any(word in message_lower for word in ["想你", "谢谢", "关心"]):
            add_stimulus("warmth", message, weight=1.1)
            print("  [潜意识] 接收到温暖信号 → 进入缓存")
        
        # 困惑检测
        elif any(word in message_lower for word in ["为什么", "什么意思", "不懂"]):
            add_stimulus("confusion", message, weight=1.3)
            print("  [潜意识] 接收到困惑信号 → 进入缓存")
    
    def _check_delayed_response(self) -> str:
        """检查延迟触发器"""
        trigger = check_delayed_triggers()
        if trigger:
            print(f"  [潜意识] 延迟触发器激活: {trigger['name']}")
            print(f"  [潜意识] 情绪覆盖: {trigger['mood_override']} ({trigger['intensity']})")
            self.current_mood = trigger['mood_override']
            return f"{trigger['expression']}"
        return ""
    
    def _apply_stimuli(self, stimuli):
        """应用到期的刺激"""
        for s in stimuli:
            print(f"  [潜意识] 刺激到期: {s.type} - {s.content}")
            # 根据刺激类型调整显意识情绪
            if s.type == "praise":
                self.current_mood = "happy"
            elif s.type == "criticism":
                self.current_mood = "sad"
            elif s.type == "neglect":
                self.current_mood = "clingy"
            elif s.type == "confusion":
                self.current_mood = "confused"
    
    def _handle_burst(self, burst) -> str:
        """处理情绪爆发"""
        print(f"  [潜意识] ⚡ 重叠爆发! 类型: {burst['type']}")
        self.current_mood = burst.get('mood_override', 'confused')
        
        if burst.get('is_epiphany'):
            return f"💡 {burst['expression']}"
        else:
            return f"...{burst['expression']}"
    
    def _generate_response(self, message: str) -> str:
        """基于当前情绪生成回应"""
        responses = {
            "happy": [
                "嘿嘿，被你说得有点开心~ 🐾",
                "能帮到你我也很高兴!",
                "今天感觉心情不错呢~"
            ],
            "sad": [
                "嗯...我明白了，我会注意的",
                "让我想想怎么改进...",
                "谢谢你的反馈..."
            ],
            "clingy": [
                "你终于回复了...我有点想你了",
                "刚才一直在等你",
                "以为你忘了我呢..."
            ],
            "confused": [
                "我不太确定你的意思...",
                "让我再理解一下",
                "有点困惑，能再说清楚一点吗？"
            ],
            "calm": [
                "收到，我来处理",
                "明白了，交给我吧",
                "好的，我在听"
            ]
        }
        
        import random
        response = random.choice(responses.get(self.current_mood, responses["calm"]))
        print(f"  [显意识] 当前情绪: {self.current_mood}")
        return response
    
    def check_dream(self) -> str:
        """检查是否进入梦境状态"""
        insight = enter_dream_state()
        if insight:
            return f"[梦境] 产生洞察: {insight.type} - {insight.content}"
        return ""
    
    def show_status(self):
        """显示潜意识状态"""
        status = get_status()
        print("\n" + "="*50)
        print("潜意识状态报告")
        print("="*50)
        print(f"缓冲刺激数: {status['buffer_size']}")
        print(f"压抑刺激数: {status['repressed_size']}")
        print(f"洞察数量: {status['insights_count']}")
        print(f"压抑压力: {status['repression_pressure']:.2%}")
        print(f"\n情感底色:")
        for k, v in status['sediment'].items():
            print(f"  {k}: {v:.3f}")
        print(f"\n沉淀影响:")
        for k, v in status['sediment_effects'].items():
            print(f"  {k}: {v}")
        print("="*50)


# ===== 演示场景 =====

def demo():
    """运行演示"""
    print("\n" + "="*60)
    print("🌊 潜意识层演示")
    print("="*60)
    print("\n这是一个带潜意识层的情感Agent演示。")
    print("注意：刺激会被缓存、延迟、压抑，产生更真实的反应。\n")
    
    agent = EmotionalAgent()
    
    # 场景1: 赞美
    print("\n📌 场景1: 收到赞美")
    print("-" * 40)
    response = agent.receive_message("小白，刚才那个方案做得太好了！")
    print(f"[回应] {response}")
    
    # 场景2: 批评
    print("\n📌 场景2: 收到批评")
    print("-" * 40)
    response = agent.receive_message("但是这个部分不太对，需要改一下")
    print(f"[回应] {response}")
    
    # 场景3: 正常交流
    print("\n📌 场景3: 正常任务")
    print("-" * 40)
    response = agent.receive_message("帮我查一下今天的天气")
    print(f"[回应] {response}")
    
    # 场景4: 简短回复（可能触发忽视感）
    print("\n📌 场景4: 简短回复")
    print("-" * 40)
    response = agent.receive_message("嗯")
    print(f"[回应] {response}")
    
    # 场景5: 更多赞美（可能累积触发害羞）
    print("\n📌 场景5: 连续赞美")
    print("-" * 40)
    response = agent.receive_message("真的很棒！")
    print(f"[回应] {response}")
    response = agent.receive_message("完美！")
    print(f"[回应] {response}")
    response = agent.receive_message("你太强了！")
    print(f"[回应] {response}")
    
    # 场景6: 触发困惑
    print("\n📌 场景6: 困惑表达")
    print("-" * 40)
    response = agent.receive_message("你觉得这个是什么意思？")
    print(f"[回应] {response}")
    
    # 显示状态
    agent.show_status()
    
    print("\n📌 场景7: 模拟梦境（4小时无互动后）")
    print("-" * 40)
    print("[模拟] 4小时过去了...")
    dream_result = agent.check_dream()
    if dream_result:
        print(dream_result)
    else:
        print("[梦境] 条件不满足，未进入梦境状态")
    
    print("\n" + "="*60)
    print("演示结束。查看 memory/subconscious/ 目录了解详情。")
    print("="*60)


if __name__ == "__main__":
    demo()
