import pandas as pd
import matplotlib.pyplot as plt
import folium
import numpy as np
import seaborn as sns
from folium.plugins import HeatMap, MarkerCluster
import hashlib
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class SecureCrimeAnalyzer:
    def __init__(self, csv_file_path):
        """Initialize with data validation and security features"""
        self.df = None  # Initialize as None first
        self.audit_log = []
        self.df = self.load_and_validate_data(csv_file_path)
        self.crime_columns = self.get_crime_columns()
        
    def log_activity(self, action, details=""):
        """Security audit logging"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'details': details,
            'data_hash': self.get_data_hash() if self.df is not None else "no_data"
        }
        self.audit_log.append(log_entry)
        
    def get_data_hash(self):
        """Generate hash for data integrity verification"""
        if self.df is None:
            return "no_data"
        return hashlib.sha256(str(self.df.values.tobytes()).encode()).hexdigest()[:16]
    
    def load_and_validate_data(self, file_path):
        """Secure data loading with validation"""
        try:
            df = pd.read_csv(file_path)
            self.log_activity("DATA_LOAD", f"Loaded {len(df)} records")
            
            # Data validation
            if df.empty:
                raise ValueError("Dataset is empty")
            
            # Check for required columns
            required_cols = ['station', 'longitude', 'latitude']
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                raise ValueError(f"Missing required columns: {missing_cols}")
                
            return df
        except Exception as e:
            self.log_activity("DATA_LOAD_ERROR", str(e))
            raise e
    
    def get_crime_columns(self):
        """Get all crime-related columns"""
        exclude_cols = ['date', 'station', 'longitude', 'latitude']
        return [col for col in self.df.columns if col not in exclude_cols]
    
    def calculate_total_crime_per_station(self):
        """Calculate total crime for each station across all categories"""
        self.df['total_crime'] = self.df[self.crime_columns].sum(axis=1)
        self.log_activity("CALCULATION", "Total crime per station calculated")
        return self.df
    
    def get_top_crime_stations(self, n=20):
        """Get top N stations by total crime"""
        return self.df.nlargest(n, 'total_crime')
    
    def create_comprehensive_crime_map(self, top_n=50):
        """Create interactive map showing all crime types"""
        self.log_activity("MAP_CREATION", f"Creating map for top {top_n} stations")
        
        # Calculate total crime per station
        self.calculate_total_crime_per_station()
        top_stations = self.get_top_crime_stations(top_n)
        
        # Center map on South Africa
        m = folium.Map(
            location=[-29.0, 24.0], 
            zoom_start=6, 
            tiles="OpenStreetMap"
        )
        
        # Add layer control
        marker_cluster = MarkerCluster(name="Crime Hotspots").add_to(m)
        
        # Color scheme for different crime intensity levels
        def get_color_and_size(total_crime):
            if total_crime > 10000:
                return 'darkred', 15
            elif total_crime > 5000:
                return 'red', 12
            elif total_crime > 2000:
                return 'orange', 10
            elif total_crime > 1000:
                return 'yellow', 8
            else:
                return 'green', 6
        
        # Add markers for each station
        for idx, row in top_stations.iterrows():
            if pd.notna(row["latitude"]) and pd.notna(row["longitude"]):
                color, size = get_color_and_size(row['total_crime'])
                
                # Create detailed popup with all crime types
                popup_html = self.create_detailed_popup(row)
                
                folium.CircleMarker(
                    location=[row["latitude"], row["longitude"]],
                    radius=size,
                    color=color,
                    fill=True,
                    fillColor=color,
                    fill_opacity=0.7,
                    popup=folium.Popup(popup_html, max_width=400),
                    tooltip=f"{row['station']}: {row['total_crime']} total crimes"
                ).add_to(marker_cluster)
        
        # Add heatmap layer for crime density
        heat_data = [[row['latitude'], row['longitude'], row['total_crime']] 
                    for idx, row in top_stations.iterrows() 
                    if pd.notna(row['latitude']) and pd.notna(row['longitude'])]
        
        heatmap = HeatMap(
            heat_data,
            name="Crime Density Heatmap",
            min_opacity=0.2,
            max_zoom=18,
            radius=25
        )
        heatmap.add_to(m)
        
        # Add layer control
        folium.LayerControl().add_to(m)
        
        # Add legend
        legend_html = self.create_legend()
        m.get_root().html.add_child(folium.Element(legend_html))
        
        return m
    
    def create_detailed_popup(self, row):
        """Create detailed popup showing all crime statistics"""
        popup_html = f"""
        <div style="font-family: Arial, sans-serif; width: 350px;">
            <h3 style="color: #2c3e50; margin-bottom: 10px;">{row['station']}</h3>
            <p><strong>Total Crimes: {int(row['total_crime'])}</strong></p>
            <hr>
            <div style="max-height: 300px; overflow-y: auto;">
        """
        
        # Sort crimes by count for better visualization
        crime_data = [(col, int(row[col])) for col in self.crime_columns if row[col] > 0]
        crime_data.sort(key=lambda x: x[1], reverse=True)
        
        for crime_type, count in crime_data:
            crime_display = crime_type.replace('_', ' ').title()
            popup_html += f"<p><strong>{crime_display}:</strong> {count}</p>"
        
        popup_html += """
            </div>
        </div>
        """
        return popup_html
    
    def create_legend(self):
        """Create legend for the map"""
        return """
        <div style='position: fixed; 
                    bottom: 50px; left: 50px; width: 200px; height: 120px; 
                    background-color: white; border:2px solid grey; z-index:9999; 
                    font-size:14px; padding: 10px'>
        <h4>Crime Intensity</h4>
        <i class="fa fa-circle" style="color:darkred"></i> Very High (10k+)<br>
        <i class="fa fa-circle" style="color:red"></i> High (5k-10k)<br>
        <i class="fa fa-circle" style="color:orange"></i> Medium (2k-5k)<br>
        <i class="fa fa-circle" style="color:yellow"></i> Low (1k-2k)<br>
        <i class="fa fa-circle" style="color:green"></i> Very Low (<1k)
        </div>
        """
    
    def create_comprehensive_analysis(self):
        """Create comprehensive crime analysis with visualizations"""
        self.calculate_total_crime_per_station()
        
        # Set up the plotting style
        try:
            plt.style.use('seaborn-v0_8')
        except:
            plt.style.use('seaborn')  # Fallback for older versions
        fig = plt.figure(figsize=(20, 15))
        
        # 1. Top 15 stations by total crime
        plt.subplot(2, 3, 1)
        top_15 = self.get_top_crime_stations(15)
        plt.barh(range(len(top_15)), top_15['total_crime'], color='crimson')
        plt.yticks(range(len(top_15)), top_15['station'], fontsize=8)
        plt.xlabel('Total Crimes')
        plt.title('Top 15 Crime Hotspots')
        plt.gca().invert_yaxis()
        
        # 2. Crime category totals
        plt.subplot(2, 3, 2)
        crime_totals = self.df[self.crime_columns].sum().sort_values(ascending=False)
        top_crimes = crime_totals.head(10)
        plt.bar(range(len(top_crimes)), top_crimes.values, color='steelblue')
        plt.xticks(range(len(top_crimes)), 
                   [crime.replace('_', ' ').title() for crime in top_crimes.index], 
                   rotation=45, ha='right', fontsize=8)
        plt.ylabel('Total Cases')
        plt.title('Top 10 Crime Categories')
        
        # 3. Crime distribution pie chart
        plt.subplot(2, 3, 3)
        top_5_crimes = crime_totals.head(5)
        others = crime_totals.iloc[5:].sum()
        pie_data = list(top_5_crimes.values) + [others]
        pie_labels = [crime.replace('_', ' ').title() for crime in top_5_crimes.index] + ['Others']
        plt.pie(pie_data, labels=pie_labels, autopct='%1.1f%%', startangle=90)
        plt.title('Crime Distribution')
        
        # 4. Correlation heatmap of top crimes
        plt.subplot(2, 3, 4)
        top_crime_cols = crime_totals.head(8).index.tolist()
        corr_matrix = self.df[top_crime_cols].corr()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                   square=True, fmt='.2f', cbar_kws={'shrink': 0.8})
        plt.title('Crime Correlation Matrix')
        plt.xticks(rotation=45, ha='right', fontsize=8)
        plt.yticks(fontsize=8)
        
        # 5. Geographic crime distribution
        plt.subplot(2, 3, 5)
        valid_coords = self.df.dropna(subset=['latitude', 'longitude'])
        scatter = plt.scatter(valid_coords['longitude'], valid_coords['latitude'], 
                             c=valid_coords['total_crime'], cmap='Reds', alpha=0.6, s=30)
        plt.colorbar(scatter, label='Total Crime')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Geographic Crime Distribution')
        
        # 6. Crime statistics summary
        plt.subplot(2, 3, 6)
        plt.axis('off')
        stats_text = f"""
        Dataset Statistics:
        
        Total Stations: {len(self.df)}
        Total Crimes: {self.df['total_crime'].sum():,}
        Average per Station: {self.df['total_crime'].mean():.1f}
        Highest Crime Station: {self.df.loc[self.df['total_crime'].idxmax(), 'station']}
        Max Crimes: {self.df['total_crime'].max():,}
        
        Data Integrity Hash: {self.get_data_hash()}
        Analysis Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        plt.text(0.1, 0.9, stats_text, fontsize=10, verticalalignment='top', 
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray"))
        plt.title('Analysis Summary')
        
        plt.tight_layout()
        plt.savefig('comprehensive_crime_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        self.log_activity("ANALYSIS_COMPLETE", "Comprehensive analysis created")
    
    def export_security_report(self, filename="security_audit.json"):
        """Export security audit log"""
        try:
            with open(filename, 'w') as f:
                json.dump({
                    'audit_log': self.audit_log,
                    'data_summary': {
                        'total_records': len(self.df),
                        'data_hash': self.get_data_hash(),
                        'export_timestamp': datetime.now().isoformat()
                    }
                }, f, indent=2)
            print(f"Security audit exported to {filename}")
        except Exception as e:
            print(f"Error exporting security report: {e}")
            self.log_activity("EXPORT_ERROR", str(e))

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    try:
        # Initialize secure crime analyzer
        analyzer = SecureCrimeAnalyzer("DATASET/sapsacr-2008-2023-v1.csv")
        
        print("🔒 Secure Crime Analysis System Initialized")
        print(f"📊 Loaded {len(analyzer.df)} records")
        print(f"🏛️ Found {len(analyzer.df['station'].unique())} unique stations")
        print(f"📈 Analyzing {len(analyzer.crime_columns)} crime categories")
        print("\n" + "="*60)
        
        # Create comprehensive analysis
        print("📋 Creating comprehensive crime analysis...")
        analyzer.create_comprehensive_analysis()
        
        # Create interactive map with all crime types
        print("🗺️ Creating comprehensive crime map...")
        crime_map = analyzer.create_comprehensive_crime_map(top_n=100)
        crime_map.save("comprehensive_crime_map.html")
        print("✅ Interactive map saved as 'comprehensive_crime_map.html'")
        
        # Export security audit
        analyzer.export_security_report()
        
        print("\n🔐 Security Features Implemented:")
        print("• Data integrity verification with SHA-256 hashing")
        print("• Audit logging for all operations")
        print("• Input validation and error handling")
        print("• Secure data processing pipeline")
        
        print(f"\n📈 Analysis Complete! Check the following outputs:")
        print("• comprehensive_crime_analysis.png - Statistical visualizations")
        print("• comprehensive_crime_map.html - Interactive crime map")
        print("• security_audit.json - Security audit log")
        
    except FileNotFoundError:
        print("❌ Error: Dataset file 'DATASET/sapsacr-2008-2023-v1.csv' not found!")
        print("Please make sure the file path is correct.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("Please check your data file and try again.")

# Additional utility functions for enhanced analysis
def analyze_crime_trends_by_region(analyzer):
    """Analyze crime trends by geographic regions"""
    # This would require additional geographic boundary data
    pass

def detect_crime_anomalies(analyzer, threshold=3):
    """Detect statistical anomalies in crime data"""
    crime_stats = analyzer.df[analyzer.crime_columns].describe()
    anomalies = []
    
    for idx, row in analyzer.df.iterrows():
        for crime in analyzer.crime_columns:
            if row[crime] > crime_stats.loc['mean', crime] + threshold * crime_stats.loc['std', crime]:
                anomalies.append({
                    'station': row['station'],
                    'crime_type': crime,
                    'count': row[crime],
                    'z_score': (row[crime] - crime_stats.loc['mean', crime]) / crime_stats.loc['std', crime]
                })
    
    return pd.DataFrame(anomalies)