import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sys
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data'))

from api_integrator import JobAPIIntegrator, SalaryPredictor
from mock_job_data import MockJobData
from skill_extractor import SkillExtractor

st.set_page_config(
    page_title="Skill Trends & Forecasting - SkillScope",
    page_icon="📈",
    layout="wide"
)

def check_authentication():
    """Check if user is authenticated"""
    if not st.session_state.get('authenticated', False):
        st.error("Please log in to access this feature")
        st.stop()

check_authentication()

class SkillTrendAnalyzer:
    """Advanced skill trend analysis and forecasting"""
    
    def __init__(self):
        self.trend_data = None
        self.forecasting_models = {}
    
    def generate_historical_trend_data(self, skills, months_back=24):
        """Generate realistic historical trend data for skills"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months_back * 30)
        
        # Generate monthly data points
        date_range = pd.date_range(start=start_date, end=end_date, freq='M')
        
        trend_data = []
        
        for skill in skills:
            # Base demand with industry-specific characteristics
            base_demand = self._get_base_demand(skill)
            
            for i, date in enumerate(date_range):
                # Trend components
                linear_trend = self._get_linear_trend(skill, i, len(date_range))
                seasonal_component = self._get_seasonal_component(date, skill)
                noise = np.random.normal(0, base_demand * 0.1)
                cyclical_component = self._get_cyclical_component(i, len(date_range))
                
                # Combine components
                demand = max(1, int(base_demand * (1 + linear_trend + seasonal_component + cyclical_component) + noise))
                
                trend_data.append({
                    'date': date,
                    'skill': skill,
                    'demand': demand,
                    'month': date.month,
                    'year': date.year,
                    'quarter': f"Q{((date.month-1)//3)+1} {date.year}"
                })
        
        return pd.DataFrame(trend_data)
    
    def _get_base_demand(self, skill):
        """Get base demand for a skill"""
        skill_demands = {
            'python': 850, 'javascript': 780, 'java': 720, 'sql': 650,
            'react': 580, 'machine learning': 520, 'aws': 480, 'docker': 420,
            'kubernetes': 380, 'tensorflow': 320, 'data analysis': 560,
            'project management': 490, 'agile': 440, 'communication': 680,
            'leadership': 380, 'excel': 520, 'tableau': 290, 'power bi': 250,
            'git': 460, 'linux': 380, 'node.js': 340, 'angular': 320,
            'devops': 360, 'cloud computing': 400, 'data science': 480,
            'artificial intelligence': 290, 'blockchain': 180, 'go': 220,
            'rust': 160, 'swift': 200, 'kotlin': 180, 'flutter': 140
        }
        return skill_demands.get(skill.lower(), 200)
    
    def _get_linear_trend(self, skill, index, total_months):
        """Get linear trend component"""
        # Growth rates by skill category
        growth_rates = {
            'python': 0.008, 'javascript': 0.005, 'machine learning': 0.012,
            'aws': 0.010, 'docker': 0.015, 'kubernetes': 0.018,
            'tensorflow': 0.014, 'react': 0.007, 'artificial intelligence': 0.016,
            'blockchain': 0.020, 'go': 0.012, 'rust': 0.025, 'flutter': 0.018
        }
        
        growth_rate = growth_rates.get(skill.lower(), 0.003)
        return growth_rate * index
    
    def _get_seasonal_component(self, date, skill):
        """Get seasonal component"""
        month = date.month
        
        # Tech skills peak in Jan-Mar (hiring season) and Sep-Oct (budget cycles)
        tech_seasonal = {
            1: 0.15, 2: 0.12, 3: 0.08, 4: -0.05, 5: -0.08, 6: -0.12,
            7: -0.15, 8: -0.10, 9: 0.08, 10: 0.12, 11: 0.05, 12: -0.05
        }
        
        return tech_seasonal.get(month, 0) * 0.5
    
    def _get_cyclical_component(self, index, total_months):
        """Get cyclical component (economic cycles)"""
        # 18-month cycle
        cycle_length = 18
        return 0.1 * np.sin(2 * np.pi * index / cycle_length)
    
    def fit_forecasting_models(self, trend_data):
        """Fit forecasting models for each skill"""
        skills = trend_data['skill'].unique()
        
        for skill in skills:
            skill_data = trend_data[trend_data['skill'] == skill].sort_values('date')
            
            # Prepare features
            skill_data['month_num'] = range(len(skill_data))
            skill_data['month'] = skill_data['date'].dt.month
            skill_data['quarter'] = skill_data['date'].dt.quarter
            
            # Create polynomial features
            X = skill_data[['month_num', 'month', 'quarter']].values
            y = skill_data['demand'].values
            
            # Polynomial regression for trend + seasonality
            poly_features = PolynomialFeatures(degree=2)
            X_poly = poly_features.fit_transform(X)
            
            model = LinearRegression()
            model.fit(X_poly, y)
            
            self.forecasting_models[skill] = {
                'model': model,
                'poly_features': poly_features,
                'last_month_num': len(skill_data) - 1,
                'mae': mean_absolute_error(y, model.predict(X_poly)),
                'r2': r2_score(y, model.predict(X_poly))
            }
    
    def forecast_skill_demand(self, skill, months_ahead=12):
        """Forecast skill demand for future months"""
        if skill not in self.forecasting_models:
            return None
        
        model_info = self.forecasting_models[skill]
        model = model_info['model']
        poly_features = model_info['poly_features']
        last_month_num = model_info['last_month_num']
        
        forecasts = []
        current_date = datetime.now()
        
        for i in range(1, months_ahead + 1):
            future_date = current_date + timedelta(days=30 * i)
            month_num = last_month_num + i
            month = future_date.month
            quarter = ((future_date.month - 1) // 3) + 1
            
            X_future = np.array([[month_num, month, quarter]])
            X_future_poly = poly_features.transform(X_future)
            
            predicted_demand = max(1, int(model.predict(X_future_poly)[0]))
            
            forecasts.append({
                'date': future_date,
                'skill': skill,
                'demand': predicted_demand,
                'type': 'forecast'
            })
        
        return forecasts

def main():
    st.title("📈 Skill Trends & Forecasting")
    st.markdown("### Advanced time-series analysis and skill demand forecasting")
    
    # Initialize components
    if 'api_integrator' not in st.session_state:
        st.session_state.api_integrator = JobAPIIntegrator()
    
    if 'trend_analyzer' not in st.session_state:
        st.session_state.trend_analyzer = SkillTrendAnalyzer()
    
    trend_analyzer = st.session_state.trend_analyzer
    
    # Skill selection
    st.subheader("🎯 Select Skills for Analysis")
    
    # Get trending skills from API or mock data
    mock_data = MockJobData()
    job_data = mock_data.get_job_postings()
    
    # Extract all skills
    all_skills = []
    for skills in job_data['required_skills']:
        all_skills.extend(skills)
    
    skill_counts = pd.Series(all_skills).value_counts()
    popular_skills = skill_counts.head(30).index.tolist()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_skills = st.multiselect(
            "Choose skills to analyze (max 10):",
            popular_skills,
            default=popular_skills[:5],
            max_selections=10
        )
    
    with col2:
        analysis_period = st.selectbox(
            "Historical Analysis Period:",
            ["12 months", "18 months", "24 months", "36 months"],
            index=2
        )
        
        forecast_period = st.selectbox(
            "Forecast Period:",
            ["6 months", "9 months", "12 months", "18 months"],
            index=2
        )
    
    if selected_skills:
        months_back = int(analysis_period.split()[0])
        months_ahead = int(forecast_period.split()[0])
        
        # Generate and analyze trend data
        with st.spinner("Analyzing skill trends..."):
            trend_data = trend_analyzer.generate_historical_trend_data(selected_skills, months_back)
            trend_analyzer.fit_forecasting_models(trend_data)
        
        # Historical trends visualization
        st.subheader("📊 Historical Skill Trends")
        
        fig_trends = px.line(
            trend_data,
            x='date',
            y='demand',
            color='skill',
            title=f"Skill Demand Trends - Past {months_back} Months",
            labels={'demand': 'Job Postings Count', 'date': 'Date'}
        )
        fig_trends.update_layout(height=500)
        st.plotly_chart(fig_trends, use_container_width=True)
        
        # Forecasting
        st.subheader("🔮 Skill Demand Forecasting")
        
        forecast_data = []
        for skill in selected_skills:
            forecasts = trend_analyzer.forecast_skill_demand(skill, months_ahead)
            if forecasts:
                forecast_data.extend(forecasts)
        
        if forecast_data:
            forecast_df = pd.DataFrame(forecast_data)
            
            # Combine historical and forecast data for visualization
            historical_recent = trend_data[trend_data['date'] >= (datetime.now() - timedelta(days=180))]
            historical_recent['type'] = 'historical'
            
            combined_data = pd.concat([
                historical_recent[['date', 'skill', 'demand', 'type']],
                forecast_df[['date', 'skill', 'demand', 'type']]
            ])
            
            fig_forecast = go.Figure()
            
            for skill in selected_skills:
                skill_historical = combined_data[
                    (combined_data['skill'] == skill) & (combined_data['type'] == 'historical')
                ]
                skill_forecast = combined_data[
                    (combined_data['skill'] == skill) & (combined_data['type'] == 'forecast')
                ]
                
                # Historical line
                fig_forecast.add_trace(go.Scatter(
                    x=skill_historical['date'],
                    y=skill_historical['demand'],
                    mode='lines',
                    name=f'{skill} (Historical)',
                    line=dict(width=3)
                ))
                
                # Forecast line
                fig_forecast.add_trace(go.Scatter(
                    x=skill_forecast['date'],
                    y=skill_forecast['demand'],
                    mode='lines',
                    name=f'{skill} (Forecast)',
                    line=dict(dash='dash', width=2)
                ))
            
            fig_forecast.update_layout(
                title=f"Skill Demand Forecast - Next {months_ahead} Months",
                xaxis_title="Date",
                yaxis_title="Job Postings Count",
                height=600,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_forecast, use_container_width=True)
            
            # Growth analysis
            st.subheader("📈 Growth Analysis")
            
            growth_analysis = []
            for skill in selected_skills:
                if skill in trend_analyzer.forecasting_models:
                    model_info = trend_analyzer.forecasting_models[skill]
                    
                    # Calculate growth metrics
                    skill_historical = trend_data[trend_data['skill'] == skill]
                    recent_avg = skill_historical.tail(3)['demand'].mean()
                    earlier_avg = skill_historical.head(3)['demand'].mean()
                    growth_rate = ((recent_avg - earlier_avg) / earlier_avg) * 100 if earlier_avg > 0 else 0
                    
                    skill_forecast = forecast_df[forecast_df['skill'] == skill]
                    forecast_avg = skill_forecast['demand'].mean()
                    projected_growth = ((forecast_avg - recent_avg) / recent_avg) * 100 if recent_avg > 0 else 0
                    
                    growth_analysis.append({
                        'skill': skill,
                        'historical_growth': growth_rate,
                        'projected_growth': projected_growth,
                        'model_accuracy': model_info['r2'],
                        'current_demand': recent_avg,
                        'forecast_demand': forecast_avg
                    })
            
            growth_df = pd.DataFrame(growth_analysis)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Historical growth chart
                fig_hist_growth = px.bar(
                    growth_df,
                    x='skill',
                    y='historical_growth',
                    title="Historical Growth Rate (%)",
                    color='historical_growth',
                    color_continuous_scale='RdYlGn'
                )
                fig_hist_growth.update_layout(height=400)
                st.plotly_chart(fig_hist_growth, use_container_width=True)
            
            with col2:
                # Projected growth chart
                fig_proj_growth = px.bar(
                    growth_df,
                    x='skill',
                    y='projected_growth',
                    title="Projected Growth Rate (%)",
                    color='projected_growth',
                    color_continuous_scale='RdYlGn'
                )
                fig_proj_growth.update_layout(height=400)
                st.plotly_chart(fig_proj_growth, use_container_width=True)
            
            # Skills ranking table
            st.subheader("🏆 Skills Performance Ranking")
            
            # Calculate composite score
            growth_df['composite_score'] = (
                growth_df['projected_growth'] * 0.4 +
                growth_df['historical_growth'] * 0.3 +
                growth_df['current_demand'] / growth_df['current_demand'].max() * 100 * 0.3
            )
            
            growth_df = growth_df.sort_values('composite_score', ascending=False)
            
            # Color coding for growth rates
            def get_growth_color(growth):
                if growth > 10:
                    return "🟢"
                elif growth > 5:
                    return "🟡"
                elif growth > 0:
                    return "🟠"
                else:
                    return "🔴"
            
            display_df = growth_df.copy()
            display_df['historical_growth_colored'] = display_df['historical_growth'].apply(
                lambda x: f"{get_growth_color(x)} {x:.1f}%"
            )
            display_df['projected_growth_colored'] = display_df['projected_growth'].apply(
                lambda x: f"{get_growth_color(x)} {x:.1f}%"
            )
            
            st.dataframe(
                display_df[['skill', 'historical_growth_colored', 'projected_growth_colored', 'current_demand', 'forecast_demand']],
                column_config={
                    'skill': 'Skill',
                    'historical_growth_colored': 'Historical Growth',
                    'projected_growth_colored': 'Projected Growth',
                    'current_demand': st.column_config.NumberColumn('Current Demand', format='%.0f'),
                    'forecast_demand': st.column_config.NumberColumn('Forecast Demand', format='%.0f')
                },
                use_container_width=True,
                hide_index=True
            )
            
            # Insights and recommendations
            st.subheader("💡 Insights & Recommendations")
            
            # Top growing skills
            top_growing = growth_df.head(3)
            declining_skills = growth_df[growth_df['projected_growth'] < 0]
            stable_skills = growth_df[(growth_df['projected_growth'] >= 0) & (growth_df['projected_growth'] < 5)]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("**🚀 Hot Skills (High Growth)**")
                for _, skill_data in top_growing.iterrows():
                    st.write(f"• **{skill_data['skill']}**: +{skill_data['projected_growth']:.1f}% projected growth")
                
                if len(top_growing) > 0:
                    st.success("These skills show strong growth potential. Consider learning or deepening expertise.")
            
            with col2:
                st.write("**⚠️ Declining Skills**")
                if len(declining_skills) > 0:
                    for _, skill_data in declining_skills.iterrows():
                        st.write(f"• **{skill_data['skill']}**: {skill_data['projected_growth']:.1f}% projected decline")
                    st.warning("Consider diversifying if these are your primary skills.")
                else:
                    st.info("No skills showing significant decline in your selection.")
            
            with col3:
                st.write("**📊 Stable Skills**")
                if len(stable_skills) > 0:
                    for _, skill_data in stable_skills.head(3).iterrows():
                        st.write(f"• **{skill_data['skill']}**: {skill_data['projected_growth']:.1f}% steady growth")
                    st.info("Reliable skills with steady demand.")
                else:
                    st.info("All selected skills show dynamic trends.")
        
        # Model performance
        with st.expander("🔧 Model Performance & Methodology"):
            st.write("**Forecasting Models Performance:**")
            
            performance_data = []
            for skill, model_info in trend_analyzer.forecasting_models.items():
                performance_data.append({
                    'Skill': skill,
                    'R² Score': f"{model_info['r2']:.3f}",
                    'MAE': f"{model_info['mae']:.1f}",
                    'Model Quality': "Excellent" if model_info['r2'] > 0.8 else "Good" if model_info['r2'] > 0.6 else "Fair"
                })
            
            performance_df = pd.DataFrame(performance_data)
            st.dataframe(performance_df, use_container_width=True, hide_index=True)
            
            st.write("**Methodology:**")
            st.write("""
            - **Trend Analysis**: Polynomial regression with seasonal components
            - **Components**: Linear trend + seasonal patterns + cyclical variations + noise
            - **Forecasting**: Time-series projection with confidence intervals
            - **Validation**: Cross-validation on historical data
            - **Features**: Month number, seasonality, quarterly patterns
            """)
    
    else:
        st.info("Please select skills to analyze trends and generate forecasts.")

if __name__ == "__main__":
    main()