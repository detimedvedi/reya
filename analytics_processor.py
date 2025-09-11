import json
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class ReyaAnalytics:
    def __init__(self, data_file='reya_complete_leaderboard.json'):
        """Initialize analytics processor with leaderboard data"""
        self.data_file = data_file
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load and preprocess the leaderboard data"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'leaderboard' in data and isinstance(data['leaderboard'], list):
                self.df = pd.DataFrame(data['leaderboard'])
                print(f"✅ Loaded {len(self.df)} users from {self.data_file}")
            else:
                raise ValueError("Invalid data format")
                
        except FileNotFoundError:
            print(f"❌ File {self.data_file} not found. Creating sample data...")
            self.create_sample_data()
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            self.create_sample_data()
    
    def create_sample_data(self):
        """Create sample data for testing"""
        np.random.seed(42)
        n_users = 10000
        
        # Generate realistic distributions
        trading_points = np.random.lognormal(8, 2, n_users)
        staking_points = np.random.lognormal(7, 1.5, n_users)
        signal_points = np.random.choice([0, 1000, 2000, 3000], n_users, p=[0.7, 0.15, 0.1, 0.05])
        
        self.df = pd.DataFrame({
            'rank': range(1, n_users + 1),
            'walletAddress': [f"0x{''.join(np.random.choice(list('0123456789abcdef'), 40))}" for _ in range(n_users)],
            'tradingPoints': trading_points,
            'stakingPoints': staking_points,
            'signalPoints': signal_points,
            'totalPoints': trading_points + staking_points + signal_points
        })
        
        # Sort by total points and update ranks
        self.df = self.df.sort_values('totalPoints', ascending=False).reset_index(drop=True)
        self.df['rank'] = range(1, len(self.df) + 1)
        
        print(f"✅ Created sample dataset with {len(self.df)} users")
    
    def basic_stats(self):
        """Generate basic statistics"""
        stats = {
            'total_users': len(self.df),
            'total_points': {
                'trading': self.df['tradingPoints'].sum(),
                'staking': self.df['stakingPoints'].sum(),
                'signal': self.df['signalPoints'].sum(),
                'total': self.df['totalPoints'].sum()
            },
            'average_points': {
                'trading': self.df['tradingPoints'].mean(),
                'staking': self.df['stakingPoints'].mean(),
                'signal': self.df['signalPoints'].mean(),
                'total': self.df['totalPoints'].mean()
            },
            'median_points': {
                'trading': self.df['tradingPoints'].median(),
                'staking': self.df['stakingPoints'].median(),
                'signal': self.df['signalPoints'].median(),
                'total': self.df['totalPoints'].median()
            },
            'top_user': {
                'wallet': self.df.iloc[0]['walletAddress'],
                'points': self.df.iloc[0]['totalPoints']
            }
        }
        return stats
    
    def user_segmentation(self):
        """Segment users into categories"""
        # Define percentiles for segmentation
        p90 = self.df['totalPoints'].quantile(0.9)
        p75 = self.df['totalPoints'].quantile(0.75)
        p50 = self.df['totalPoints'].quantile(0.5)
        p25 = self.df['totalPoints'].quantile(0.25)
        
        def categorize_user(points):
            if points >= p90:
                return 'Whale (Top 10%)'
            elif points >= p75:
                return 'High Performer (75-90%)'
            elif points >= p50:
                return 'Active User (50-75%)'
            elif points >= p25:
                return 'Regular User (25-50%)'
            else:
                return 'New User (Bottom 25%)'
        
        self.df['user_category'] = self.df['totalPoints'].apply(categorize_user)
        
        segmentation = self.df['user_category'].value_counts()
        return segmentation.to_dict()
    
    def strategy_analysis(self):
        """Analyze user strategies based on point distribution"""
        # Calculate point ratios
        self.df['trading_ratio'] = self.df['tradingPoints'] / self.df['totalPoints']
        self.df['staking_ratio'] = self.df['stakingPoints'] / self.df['totalPoints']
        self.df['signal_ratio'] = self.df['signalPoints'] / self.df['totalPoints']
        
        # Define strategy categories
        def categorize_strategy(row):
            if row['trading_ratio'] > 0.7:
                return 'Trading Focused'
            elif row['staking_ratio'] > 0.7:
                return 'Staking Focused'
            elif row['signal_ratio'] > 0.3:
                return 'Signal Focused'
            elif row['trading_ratio'] > 0.4 and row['staking_ratio'] > 0.4:
                return 'Balanced'
            else:
                return 'Mixed Strategy'
        
        self.df['strategy'] = self.df.apply(categorize_strategy, axis=1)
        
        strategy_stats = {}
        for strategy in self.df['strategy'].unique():
            strategy_users = self.df[self.df['strategy'] == strategy]
            strategy_stats[strategy] = {
                'count': len(strategy_users),
                'avg_total_points': strategy_users['totalPoints'].mean(),
                'avg_trading_points': strategy_users['tradingPoints'].mean(),
                'avg_staking_points': strategy_users['stakingPoints'].mean(),
                'avg_signal_points': strategy_users['signalPoints'].mean()
            }
        
        return strategy_stats
    
    def top_performers_analysis(self, top_n=100):
        """Analyze top performers"""
        top_users = self.df.head(top_n)
        
        analysis = {
            'top_traders': top_users.nlargest(10, 'tradingPoints')[['walletAddress', 'tradingPoints', 'totalPoints']].to_dict('records'),
            'top_stakers': top_users.nlargest(10, 'stakingPoints')[['walletAddress', 'stakingPoints', 'totalPoints']].to_dict('records'),
            'top_signalers': top_users.nlargest(10, 'signalPoints')[['walletAddress', 'signalPoints', 'totalPoints']].to_dict('records'),
            'strategy_distribution': top_users['strategy'].value_counts().to_dict(),
            'average_points': {
                'trading': top_users['tradingPoints'].mean(),
                'staking': top_users['stakingPoints'].mean(),
                'signal': top_users['signalPoints'].mean(),
                'total': top_users['totalPoints'].mean()
            }
        }
        
        return analysis
    
    def correlation_analysis(self):
        """Analyze correlations between different point types"""
        correlations = self.df[['tradingPoints', 'stakingPoints', 'signalPoints', 'totalPoints']].corr()
        return correlations.to_dict()
    
    def generate_insights(self):
        """Generate key insights from the data"""
        insights = []
        
        # Basic stats
        stats = self.basic_stats()
        insights.append(f"📊 Total participants: {stats['total_users']:,}")
        insights.append(f"💰 Total points distributed: {stats['total_points']['total']:,.0f}")
        insights.append(f"📈 Average points per user: {stats['average_points']['total']:,.0f}")
        
        # Point distribution
        trading_pct = (stats['total_points']['trading'] / stats['total_points']['total']) * 100
        staking_pct = (stats['total_points']['staking'] / stats['total_points']['total']) * 100
        signal_pct = (stats['total_points']['signal'] / stats['total_points']['total']) * 100
        
        insights.append(f"🎯 Point distribution: Trading {trading_pct:.1f}%, Staking {staking_pct:.1f}%, Signal {signal_pct:.1f}%")
        
        # User segmentation
        segmentation = self.user_segmentation()
        whale_count = segmentation.get('Whale (Top 10%)', 0)
        insights.append(f"🐋 Whales (top 10%): {whale_count:,} users")
        
        # Strategy analysis
        strategy_stats = self.strategy_analysis()
        most_common_strategy = max(strategy_stats.keys(), key=lambda x: strategy_stats[x]['count'])
        insights.append(f"🎮 Most common strategy: {most_common_strategy} ({strategy_stats[most_common_strategy]['count']:,} users)")
        
        # Top performer insights
        top_analysis = self.top_performers_analysis()
        top_trader = top_analysis['top_traders'][0]
        insights.append(f"🏆 Top trader: {top_trader['walletAddress'][:10]}... with {top_trader['tradingPoints']:,.0f} trading points")
        
        return insights
    
    def export_summary_report(self, filename='reya_analytics_report.json'):
        """Export comprehensive analytics report"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'data_source': self.data_file,
            'basic_stats': self.basic_stats(),
            'user_segmentation': self.user_segmentation(),
            'strategy_analysis': self.strategy_analysis(),
            'top_performers': self.top_performers_analysis(),
            'correlations': self.correlation_analysis(),
            'key_insights': self.generate_insights()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ Analytics report exported to {filename}")
        return report
    
    def create_visualizations(self):
        """Create visualization plots"""
        try:
            plt.style.use('seaborn-v0_8')
        except:
            # Fallback if seaborn style not available
            plt.style.use('default')
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Reya Chain Points Analytics Dashboard', fontsize=16, fontweight='bold')
        
        # 1. Points distribution histogram
        axes[0, 0].hist(self.df['totalPoints'], bins=50, alpha=0.7, color='skyblue', edgecolor='black')
        axes[0, 0].set_title('Total Points Distribution')
        axes[0, 0].set_xlabel('Total Points')
        axes[0, 0].set_ylabel('Number of Users')
        axes[0, 0].set_yscale('log')
        
        # 2. Points by category pie chart
        point_sums = [
            self.df['tradingPoints'].sum(),
            self.df['stakingPoints'].sum(),
            self.df['signalPoints'].sum()
        ]
        axes[0, 1].pie(point_sums, labels=['Trading', 'Staking', 'Signal'], autopct='%1.1f%%', startangle=90)
        axes[0, 1].set_title('Points Distribution by Category')
        
        # 3. User segmentation
        segmentation = self.user_segmentation()
        axes[0, 2].bar(segmentation.keys(), segmentation.values(), color=['#FFD700', '#C0C0C0', '#CD7F32', 'lightblue', 'lightgray'])
        axes[0, 2].set_title('User Segmentation')
        axes[0, 2].set_ylabel('Number of Users')
        axes[0, 2].tick_params(axis='x', rotation=45)
        
        # 4. Trading vs Staking scatter plot
        sample_df = self.df.sample(min(1000, len(self.df)))  # Sample for performance
        axes[1, 0].scatter(sample_df['tradingPoints'], sample_df['stakingPoints'], alpha=0.6, s=20)
        axes[1, 0].set_title('Trading vs Staking Points')
        axes[1, 0].set_xlabel('Trading Points')
        axes[1, 0].set_ylabel('Staking Points')
        
        # 5. Strategy distribution
        strategy_stats = self.strategy_analysis()
        strategies = list(strategy_stats.keys())
        counts = [strategy_stats[s]['count'] for s in strategies]
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'][:len(strategies)]
        axes[1, 1].bar(strategies, counts, color=colors)
        axes[1, 1].set_title('Strategy Distribution')
        axes[1, 1].set_ylabel('Number of Users')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        # 6. Top 50 users
        top_50 = self.df.head(50)
        axes[1, 2].plot(range(1, 51), top_50['totalPoints'], marker='o', linewidth=2, markersize=4)
        axes[1, 2].set_title('Top 50 Users Points')
        axes[1, 2].set_xlabel('Rank')
        axes[1, 2].set_ylabel('Total Points')
        
        plt.tight_layout()
        
        try:
            plt.savefig('reya_analytics_dashboard.png', dpi=300, bbox_inches='tight')
            print("✅ Visualizations saved as 'reya_analytics_dashboard.png'")
        except Exception as e:
            print(f"⚠️  Could not save visualization: {e}")
        
        try:
            plt.show()
        except Exception as e:
            print(f"⚠️  Could not display plots: {e}")
            print("   This is normal when running without a display (e.g., in some terminals)")

def main():
    """Main function to run analytics"""
    print("🚀 Starting Reya Chain Points Analytics...")
    
    # Initialize analytics
    analytics = ReyaAnalytics()
    
    # Generate insights
    print("\n📈 Key Insights:")
    insights = analytics.generate_insights()
    for insight in insights:
        print(f"  {insight}")
    
    # Export comprehensive report
    print("\n📊 Generating comprehensive report...")
    report = analytics.export_summary_report()
    
    # Create visualizations (optional - requires matplotlib)
    try:
        print("\n📈 Creating visualizations...")
        analytics.create_visualizations()
    except ImportError:
        print("⚠️  Matplotlib not available. Skipping visualizations.")
        print("   Install with: pip install matplotlib seaborn")
    
    print("\n✅ Analytics complete!")
    return analytics

if __name__ == "__main__":
    main()
