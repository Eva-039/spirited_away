#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spirited Away Script Analysis
千与千寻剧本分析工具
"""

import re
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import numpy as np
import seaborn as sns
import networkx as nx

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class SpiritedAwayAnalyzer:
    def __init__(self, script_file):
        """初始化分析器"""
        self.script_file = script_file
        self.script_text = ""
        self.lines = []
        self.characters = {}
        
    def load_script(self):
        """加载剧本文件"""
        try:
            with open(self.script_file, 'r', encoding='utf-8') as f:
                self.script_text = f.read()
            self.lines = self.script_text.split('\n')
            print(f"✅ 成功加载剧本，共 {len(self.lines)} 行")
            return True
        except Exception as e:
            print(f"❌ 加载剧本失败: {e}")
            return False
    
    def extract_characters(self):
        """提取主要角色和台词"""
        # 主要角色列表
        main_characters = [
            'Chihiro', 'Haku', 'Yobaba', 'Zeniba', 'Rin', 
            'No Face', 'Grandpa Kama', 'Mom', 'Dad'
        ]
        
        character_lines = {char: [] for char in main_characters}
        character_count = {char: 0 for char in main_characters}
        
        for line in self.lines:
            line = line.strip()
            if line and not line.startswith('<') and not line.startswith('*'):
                # 检查是否包含角色名
                for char in main_characters:
                    if char.lower() in line.lower():
                        character_lines[char].append(line)
                        character_count[char] += 1
        
        self.characters = character_count
        return character_lines, character_count
    
    def create_wordcloud(self):
        """生成词云图"""
        # 清理文本
        text = self.script_text.lower()
        # 移除特殊标记
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'\*[^*]+\*', '', text)
        text = re.sub(r'\[[^\]]+\]', '', text)
        
        # 常见停用词
        stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us',
            'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their', 'this', 
            'that', 'these', 'those', 'what', 'where', 'when', 'why', 'how',
            'timer', 'missed', 'line', 'check', 'illusion', 'sounds', 'like'
        }
        
        # 生成词云
        wordcloud = WordCloud(
            width=800, 
            height=400, 
            background_color='white',
            stopwords=stopwords,
            max_words=100,
            colormap='viridis'
        ).generate(text)
        
        plt.figure(figsize=(12, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Spirited Away - Key Words Cloud\n千与千寻关键词云', fontsize=16, pad=20)
        plt.tight_layout()
        plt.savefig('spirited_away_wordcloud.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("✅ 词云图已生成: spirited_away_wordcloud.png")
    
    def analyze_characters(self):
        """分析角色出场频率"""
        character_lines, character_count = self.extract_characters()
        
        # 过滤掉出场次数为0的角色
        filtered_chars = {k: v for k, v in character_count.items() if v > 0}
        
        # 创建角色分析图
        plt.figure(figsize=(12, 8))
        
        # 角色出场频率条形图
        chars = list(filtered_chars.keys())
        counts = list(filtered_chars.values())
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(chars)))
        bars = plt.bar(chars, counts, color=colors)
        
        plt.title('Character Appearance Frequency in Spirited Away\n千与千寻角色出场频率分析', fontsize=14, pad=20)
        plt.xlabel('Characters 角色', fontsize=12)
        plt.ylabel('Appearance Count 出场次数', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        
        # 添加数值标签
        for bar, count in zip(bars, counts):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                    str(count), ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        plt.savefig('character_frequency.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("✅ 角色分析图已生成: character_frequency.png")
        
        return filtered_chars
    
    def sentiment_analysis(self):
        """简单情感分析"""
        # 定义情感词汇
        positive_words = [
            'good', 'great', 'wonderful', 'beautiful', 'happy', 'love', 'nice',
            'amazing', 'fantastic', 'excellent', 'perfect', 'thank', 'thanks'
        ]
        
        negative_words = [
            'bad', 'terrible', 'awful', 'sad', 'angry', 'hate', 'horrible',
            'scary', 'afraid', 'worried', 'sorry', 'hurt', 'pain', 'die'
        ]
        
        # 按段落分析情感
        segments = []
        sentiment_scores = []
        
        # 将剧本分成10个段落
        total_lines = len(self.lines)
        segment_size = total_lines // 10
        
        for i in range(10):
            start = i * segment_size
            end = start + segment_size if i < 9 else total_lines
            segment_text = ' '.join(self.lines[start:end]).lower()
            
            pos_count = sum(1 for word in positive_words if word in segment_text)
            neg_count = sum(1 for word in negative_words if word in segment_text)
            
            # 计算情感分数 (-1 到 1)
            total_emotional_words = pos_count + neg_count
            if total_emotional_words > 0:
                sentiment = (pos_count - neg_count) / total_emotional_words
            else:
                sentiment = 0
            
            segments.append(f"Segment {i+1}")
            sentiment_scores.append(sentiment)
        
        # 绘制情感变化图
        plt.figure(figsize=(12, 6))
        plt.plot(range(1, 11), sentiment_scores, marker='o', linewidth=2, markersize=8)
        plt.axhline(y=0, color='gray', linestyle='--', alpha=0.7)
        plt.title('Emotional Journey in Spirited Away\n千与千寻情感变化曲线', fontsize=14, pad=20)
        plt.xlabel('Story Segments 故事段落', fontsize=12)
        plt.ylabel('Sentiment Score 情感分数', fontsize=12)
        plt.ylim(-1, 1)
        plt.grid(True, alpha=0.3)
        
        # 添加情感区域标注
        plt.fill_between(range(1, 11), sentiment_scores, 0, 
                        where=[s >= 0 for s in sentiment_scores], 
                        color='green', alpha=0.3, label='Positive 积极')
        plt.fill_between(range(1, 11), sentiment_scores, 0, 
                        where=[s < 0 for s in sentiment_scores], 
                        color='red', alpha=0.3, label='Negative 消极')
        
        plt.legend()
        plt.tight_layout()
        plt.savefig('sentiment_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("✅ 情感分析图已生成: sentiment_analysis.png")
        
        return segments, sentiment_scores

    def create_character_network(self):
        """创建人物关系网络图"""
        # 主要角色
        main_characters = ['Chihiro', 'Haku', 'Yobaba', 'Zeniba', 'Rin', 'No Face', 'Grandpa Kama']

        # 创建网络图
        G = nx.Graph()

        # 添加节点
        for char in main_characters:
            G.add_node(char)

        # 定义角色关系（基于剧情）
        relationships = [
            ('Chihiro', 'Haku', 3),      # 主要关系
            ('Chihiro', 'Yobaba', 2),    # 雇佣关系
            ('Chihiro', 'Rin', 2),       # 友谊
            ('Chihiro', 'No Face', 2),   # 帮助关系
            ('Chihiro', 'Grandpa Kama', 1), # 求助关系
            ('Haku', 'Yobaba', 2),       # 仆从关系
            ('Yobaba', 'Zeniba', 1),     # 姐妹关系
            ('Rin', 'Grandpa Kama', 1),  # 工作关系
            ('Chihiro', 'Zeniba', 1),    # 拜访关系
        ]

        # 添加边
        for char1, char2, weight in relationships:
            if char1 in main_characters and char2 in main_characters:
                G.add_edge(char1, char2, weight=weight)

        # 绘制网络图
        plt.figure(figsize=(12, 10))

        # 设置布局
        pos = nx.spring_layout(G, k=3, iterations=50)

        # 绘制节点
        node_sizes = [G.degree(node) * 500 + 1000 for node in G.nodes()]
        nx.draw_networkx_nodes(G, pos, node_size=node_sizes,
                              node_color='lightblue', alpha=0.7)

        # 绘制边
        edges = G.edges()
        weights = [G[u][v]['weight'] for u, v in edges]
        nx.draw_networkx_edges(G, pos, width=[w*2 for w in weights],
                              alpha=0.6, edge_color='gray')

        # 添加标签
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

        plt.title('Character Relationship Network in Spirited Away\n千与千寻人物关系网络图',
                 fontsize=14, pad=20)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig('character_network.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("✅ 人物关系网络图已生成: character_network.png")

        return G
    
    def generate_summary_report(self):
        """生成分析报告"""
        print("\n" + "="*50)
        print("📊 SPIRITED AWAY SCRIPT ANALYSIS REPORT")
        print("千与千寻剧本分析报告")
        print("="*50)
        
        print(f"📝 Script Length: {len(self.lines)} lines")
        print(f"📝 剧本长度: {len(self.lines)} 行")
        
        character_lines, character_count = self.extract_characters()
        filtered_chars = {k: v for k, v in character_count.items() if v > 0}
        
        print(f"\n👥 Main Characters Detected: {len(filtered_chars)}")
        print("👥 检测到的主要角色:")
        for char, count in sorted(filtered_chars.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {char}: {count} appearances")
        
        print(f"\n🎭 Most Active Character: {max(filtered_chars, key=filtered_chars.get)}")
        print(f"🎭 最活跃角色: {max(filtered_chars, key=filtered_chars.get)}")
        
        print("\n✅ Generated Visualizations:")
        print("✅ 已生成可视化图表:")
        print("   • spirited_away_wordcloud.png - Word Cloud")
        print("   • character_frequency.png - Character Analysis")
        print("   • sentiment_analysis.png - Emotional Journey")
        
        return True

def main():
    """主函数"""
    print("🎬 Starting Spirited Away Script Analysis...")
    print("🎬 开始千与千寻剧本分析...")
    
    # 初始化分析器
    analyzer = SpiritedAwayAnalyzer('剧本.txt')
    
    # 加载剧本
    if not analyzer.load_script():
        return
    
    # 执行分析
    print("\n📊 Generating visualizations...")
    analyzer.create_wordcloud()
    analyzer.analyze_characters()
    analyzer.sentiment_analysis()
    analyzer.create_character_network()
    
    # 生成报告
    analyzer.generate_summary_report()
    
    print("\n🎉 Analysis completed! Ready for Wix website.")
    print("🎉 分析完成！可以用于Wix网站了。")

if __name__ == "__main__":
    main()
