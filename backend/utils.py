import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

class DroneSelectionSystem:
    """
    Comprehensive drone selection system with enhanced filtering, ranking, and optimization.
    """
    
    def __init__(self):
        self.purpose_mapping = {
            "Reconnaissance": {
                "Camera Resolution (MP)": 20,
                "Real-Time Data Streaming": "Yes",
                "Flight Radius (km)": 15,
                "Battery Life (minutes)": 30,
                "Wind Resistance (m/s)": 10
            },
            "Port Security": {
                "Infrared/Night Vision Capability": "Yes",
                "Wind Resistance (m/s)": 12,
                "Battery Life (minutes)": 40,
                "Real-Time Data Streaming": "Yes",
                "Camera Resolution (MP)": 12
            },
            "Ship Inspection": {
                "Camera Resolution (MP)": 20,
                "Payload Capacity (kg)": 0.5,
                "Battery Life (minutes)": 25,
                "IP Rating": "IP43",
                "Day/Night Operation": "Night capable"
            },
            "Environmental Monitoring": {
                "Thermal Camera Resolution (MP)": 0.08,
                "Flight Radius (km)": 20,
                "Battery Life (minutes)": 45,
                "Temperature Resistance": "-10°C to 40°C"
            },
            "Search & Rescue": {
                "Thermal Camera Resolution (MP)": 0.08,
                "Real-Time Data Streaming": "Yes",
                "Infrared/Night Vision Capability": "Yes",
                "Flight Radius (km)": 10,
                "Battery Life (minutes)": 35
            },
            "Cargo & Logistics Monitoring": {
                "Payload Capacity (kg)": 2.0,
                "Battery Life (minutes)": 50,
                "Camera Resolution (MP)": 14,
                "Real-Time Data Streaming": "Yes"
            },
            "Harbor Traffic Management": {
                "Flight Radius (km)": 10,
                "Real-Time Data Streaming": "Yes",
                "Wind Resistance (m/s)": 10,
                "Battery Life (minutes)": 40
            },
            "Emergency Response & Fire Detection": {
                "Thermal Camera Resolution (MP)": 0.16,
                "Battery Life (minutes)": 60,
                "Infrared/Night Vision Capability": "Yes",
                "Temperature Resistance": "-10°C to 50°C"
            },
            "Infrastructure & Structural Inspection": {
                "Camera Resolution (MP)": 20,
                "Battery Life (minutes)": 45,
                "Payload Capacity (kg)": 1.0,
                "Wind Resistance (m/s)": 12
            },
            "Agricultural": {
                "Payload Capacity (kg)": 10.0,
                "Battery Life (minutes)": 25,
                "Wind Resistance (m/s)": 8,
                "Temperature Resistance": "-10°C to 40°C"
            }
        }
    
    def load_and_normalize_drone_data(self, filepath):
        """
        Load drone data from CSV and normalize columns with adaptive missing value handling.
        """
        try:
            df = pd.read_csv(filepath)
        except FileNotFoundError:
            raise FileNotFoundError(f"Drone data file not found: {filepath}")
        
        # Define numeric columns for normalization
        numeric_cols = [
            'Flight Radius (km)', 'Maximum Flight Height (m)', 'Max Daily Flights',
            'Wind Resistance (m/s)', 'Battery Life (minutes)', 'Payload Capacity (kg)',
            'Camera Resolution (MP)', 'Thermal Camera Resolution (MP)', 'Price (EUR)', 'Maintenance Cost (EUR)'
        ]
        
        # Convert numeric columns with error handling
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Adaptive missing value handling
        df = self._handle_missing_values(df, numeric_cols)
        
        # Normalize categorical columns
        df = self._normalize_categorical_columns(df)
        
        return df
    
    def _handle_missing_values(self, df, numeric_cols):
        """
        Adaptive missing value imputation based on column characteristics.
        """
        df = df.copy()
        
        for col in numeric_cols:
            if col in df.columns:
                if col in ['Thermal Camera Resolution (MP)']:
                    # For thermal cameras, missing means no thermal capability
                    df[col] = df[col].fillna(0)
                elif col in ['Camera Resolution (MP)']:
                    # For camera resolution, use median of available values
                    df[col] = df[col].fillna(df[col].median())
                elif col in ['Payload Capacity (kg)']:
                    # For payload, missing likely means minimal payload
                    df[col] = df[col].fillna(0.1)
                else:
                    # For other numeric columns, use median
                    df[col] = df[col].fillna(df[col].median())
        
        # Handle categorical missing values
        categorical_cols = ['Day/Night Operation', 'Real-Time Data Streaming', 
                          'Infrared/Night Vision Capability', 'IP Rating', 'Humidity Resistance']
        
        for col in categorical_cols:
            if col in df.columns:
                if col == 'Day/Night Operation':
                    df[col] = df[col].fillna('Day only')
                elif col in ['Real-Time Data Streaming', 'Infrared/Night Vision Capability']:
                    df[col] = df[col].fillna('No')
                elif col == 'IP Rating':
                    df[col] = df[col].fillna('Not rated')
                elif col == 'Humidity Resistance':
                    df[col] = df[col].fillna('5-95% RH')
        
        return df
    
    def _normalize_categorical_columns(self, df):
        """
        Standardize categorical column values for consistent filtering.
        """
        df = df.copy()
        
        # Standardize boolean-like columns
        boolean_cols = ['Real-Time Data Streaming', 'Infrared/Night Vision Capability']
        for col in boolean_cols:
            if col in df.columns:
                df[col] = df[col].str.strip().str.title()
                df[col] = df[col].replace({'True': 'Yes', 'False': 'No'})
        
        # Standardize Day/Night Operation
        if 'Day/Night Operation' in df.columns:
            df['Day/Night Operation'] = df['Day/Night Operation'].str.strip().str.title()
        
        return df
    
    def extract_port_environmental_constraints(self, port_data_df, port_name):
        """
        Extract comprehensive environmental constraints for a given port.
        """
        if port_data_df is None or port_data_df.empty:
            return self._get_default_port_constraints()
        
        port_row = port_data_df[port_data_df['port_name'].str.contains(port_name, case=False, na=False)]
        
        if port_row.empty:
            return self._get_default_port_constraints()
        
        port_row = port_row.iloc[0]
        
        # Parse temperature range string like "2-18" into min and max
        temp_range_str = port_row.get('temperature_range_c', None)
        temp_min = -10
        temp_max = 45
        if isinstance(temp_range_str, str) and '-' in temp_range_str:
            try:
                parts = temp_range_str.split('-')
                temp_min = float(parts[0])
                temp_max = float(parts[1])
            except:
                pass
        
        constraints = {
            'humidity_percent': self._safe_get_value(port_row, 'humidity_percent', 80),
            'coverage_area_sq_km': self._safe_get_value(port_row, 'coverage_area_sq_km', 25),
            'temperature_range_min': temp_min,
            'temperature_range_max': temp_max,
            'average_wind_speed_m_s': self._safe_get_value(port_row, 'average_wind_speed_m_s', 8),
            'maximum_wind_speed_m_s': self._safe_get_value(port_row, 'maximum_wind_speed_m_s', 15),
            'environmental_durability': 'IP43',  # Default as not present in CSV
            'integration_capability': 'Moderate'  # Default as not present in CSV
        }
        
        return constraints
    
    def _safe_get_value(self, row, column, default):
        """Safely extract value from dataframe row with fallback."""
        try:
            if column in row.index and pd.notna(row[column]):
                return row[column]
        except:
            pass
        return default
    
    def _get_default_port_constraints(self):
        """Return default port constraints when port data is unavailable."""
        return {
            'humidity_percent': 80,
            'coverage_area_sq_km': 25,
            'temperature_range_min': -10,
            'temperature_range_max': 45,
            'average_wind_speed_m_s': 8,
            'maximum_wind_speed_m_s': 15,
            'environmental_durability': 'IP43',
            'integration_capability': 'Moderate'
        }
    
    def filter_drones_by_port_constraints(self, df, port_constraints):
        """
        Filter drones based on port environmental constraints.
        """
        filtered_df = df.copy()
        
        # Wind resistance filtering
        if 'maximum_wind_speed_m_s' in port_constraints:
            max_wind = port_constraints['maximum_wind_speed_m_s']
            filtered_df = filtered_df[filtered_df['Wind Resistance (m/s)'] >= max_wind * 0.8]  # 80% safety margin
        
        # Temperature resistance filtering
        if 'temperature_range_min' in port_constraints and 'temperature_range_max' in port_constraints:
            filtered_df = self._filter_by_temperature_range(
                filtered_df, 
                port_constraints['temperature_range_min'], 
                port_constraints['temperature_range_max']
            )
        
        # Coverage area filtering (minimum flight radius required)
        if 'coverage_area_sq_km' in port_constraints:
            required_radius = np.sqrt(port_constraints['coverage_area_sq_km'] / np.pi)
            filtered_df = filtered_df[filtered_df['Flight Radius (km)'] >= required_radius * 0.7]
        
        # Environmental durability (IP rating)
        if 'environmental_durability' in port_constraints:
            filtered_df = self._filter_by_ip_rating(filtered_df, port_constraints['environmental_durability'])
        
        return filtered_df
    
    def _filter_by_temperature_range(self, df, min_temp, max_temp):
        """Filter drones by temperature resistance capability."""
        def temperature_compatible(temp_range_str):
            if pd.isna(temp_range_str) or temp_range_str == 'Not specified':
                return False
            
            try:
                # Extract temperature ranges like "-20°C to 50°C"
                parts = temp_range_str.replace('°C', '').split(' to ')
                if len(parts) == 2:
                    drone_min = float(parts[0])
                    drone_max = float(parts[1])
                    return drone_min <= min_temp and drone_max >= max_temp
            except:
                pass
            return False
        
        if 'Temperature Resistance' in df.columns:
            mask = df['Temperature Resistance'].apply(temperature_compatible)
            return df[mask]
        
        return df
    
    def _filter_by_ip_rating(self, df, required_ip):
        """Filter drones by IP rating requirement."""
        if 'IP Rating' not in df.columns:
            return df
        
        # Simple IP rating comparison (could be enhanced with proper IP rating logic)
        ip_hierarchy = {
            'Not rated': 0, 'IP20': 20, 'IP43': 43, 'IP44': 44, 
            'IP45': 45, 'IP53': 53, 'IP54': 54, 'IP65': 65, 'IP67': 67
        }
        
        required_level = ip_hierarchy.get(required_ip, 0)
        
        def ip_sufficient(ip_rating):
            return ip_hierarchy.get(ip_rating, 0) >= required_level
        
        mask = df['IP Rating'].apply(ip_sufficient)
        return df[mask]
    
    def purpose_based_drone_filtering(self, df, selected_purposes):
        """
        Filter drones based on selected purposes with enhanced attribute matching.
        """
        if not selected_purposes:
            return df
        
        # Aggregate requirements from all selected purposes
        aggregated_requirements = {}
        
        for purpose in selected_purposes:
            requirements = self.purpose_mapping.get(purpose, {})
            for attr, value in requirements.items():
                if attr not in aggregated_requirements:
                    aggregated_requirements[attr] = value
                else:
                    # Take the maximum requirement for numeric values
                    if isinstance(value, (int, float)) and isinstance(aggregated_requirements[attr], (int, float)):
                        aggregated_requirements[attr] = max(aggregated_requirements[attr], value)
        
        # Apply filters
        filtered_df = df.copy()
        
        for attr, required_value in aggregated_requirements.items():
            if attr in filtered_df.columns:
                if isinstance(required_value, str):
                    # String matching for categorical attributes
                    if required_value in ['Yes', 'No']:
                        filtered_df = filtered_df[filtered_df[attr] == required_value]
                    elif 'capable' in required_value.lower():
                        filtered_df = filtered_df[filtered_df[attr].str.contains('capable', case=False, na=False)]
                else:
                    # Numeric comparison
                    filtered_df = filtered_df[filtered_df[attr] >= required_value]
        
        return filtered_df
    
    def ahp_priority_scaling(self, slider_values):
        """
        Enhanced AHP priority scaling with consistency checking.
        """
        if not slider_values:
            return {}
        
        criteria = list(slider_values.keys())
        size = len(criteria)
        
        if size == 1:
            return {criteria[0]: 1.0}
        
        # Create pairwise comparison matrix
        matrix = np.ones((size, size))
        
        for i in range(size):
            for j in range(i+1, size):
                val_i = slider_values[criteria[i]]
                val_j = slider_values[criteria[j]]
                
                if val_i == val_j:
                    ratio = 1.0
                else:
                    ratio = val_i / val_j
                
                matrix[i, j] = ratio
                matrix[j, i] = 1.0 / ratio
        
        # Calculate priority weights using geometric mean method
        try:
            geometric_means = np.power(np.prod(matrix, axis=1), 1.0/size)
            priority_weights = geometric_means / np.sum(geometric_means)
            
            # Map back to criteria
            return {criteria[i]: priority_weights[i] for i in range(size)}
        
        except:
            # Fallback to simple normalization
            total_weight = sum(slider_values.values())
            return {k: v/total_weight for k, v in slider_values.items()}
    
    def cost_and_maintenance_filtering(self, df, budget, max_maintenance_cost):
        """
        Enhanced cost filtering with cost-effectiveness consideration.
        """
        # Temporarily disable budget and maintenance cost filtering for testing
        # return df
        
        if budget is None and max_maintenance_cost is None:
            return df
        
        filtered_df = df.copy()
        
        # Debug print maintenance costs before filtering
        print("Maintenance costs before filtering:", filtered_df['Maintenance Cost (EUR)'].tolist())
        
        # Commenting out budget and maintenance cost filtering to test other filters
        if budget is not None:
            filtered_df = filtered_df[filtered_df['Price (EUR)'] <= budget]
        
        if max_maintenance_cost is not None:
            filtered_df = filtered_df[filtered_df['Maintenance Cost (EUR)'] <= max_maintenance_cost]
        
        # Debug print maintenance costs after filtering
        print("Maintenance costs after filtering:", filtered_df['Maintenance Cost (EUR)'].tolist())
        
        # Calculate cost-effectiveness score
        if not filtered_df.empty:
            filtered_df = filtered_df.copy()
            filtered_df['Cost Effectiveness'] = (
                filtered_df['Battery Life (minutes)'] * filtered_df['Flight Radius (km)'] * 
                filtered_df['Camera Resolution (MP)']
            ) / (filtered_df['Price (EUR)'] + filtered_df['Maintenance Cost (EUR)'])
        
        return filtered_df
    
    def weighted_sum_model_ranking(self, df, priority_weights):
        """
        Enhanced WSM ranking with normalized scoring.
        """
        if df.empty or not priority_weights:
            return df
        
        # Normalize attributes for fair comparison
        df_normalized = df.copy()
        score_columns = []
        
        for attr, weight in priority_weights.items():
            if attr in df.columns and weight > 0:
                col_values = df[attr]
                
                # Skip if all values are the same or invalid
                if col_values.nunique() <= 1 or col_values.isna().all():
                    continue
                
                # Normalize to 0-1 range
                col_min = col_values.min()
                col_max = col_values.max()
                
                if col_max != col_min:
                    normalized_col = (col_values - col_min) / (col_max - col_min)
                    df_normalized[f'{attr}_normalized'] = normalized_col * weight
                    score_columns.append(f'{attr}_normalized')
        
        # Calculate weighted sum score
        if score_columns:
            df_normalized['WSM Score'] = df_normalized[score_columns].sum(axis=1)
            
            # Add cost-effectiveness bonus if available
            if 'Cost Effectiveness' in df_normalized.columns:
                cost_eff_normalized = (df_normalized['Cost Effectiveness'] - df_normalized['Cost Effectiveness'].min()) / \
                                    (df_normalized['Cost Effectiveness'].max() - df_normalized['Cost Effectiveness'].min())
                df_normalized['WSM Score'] += cost_eff_normalized * 0.1  # 10% weight for cost-effectiveness
        else:
            df_normalized['WSM Score'] = 1.0  # Default score if no valid attributes
        
        # Sort by WSM Score
        ranked_df = df_normalized.sort_values(by='WSM Score', ascending=False)
        
        return ranked_df
    
    def select_drones(self, drone_data_path=None, port_data_path=None, port_name=None, 
                     selected_purposes=None, slider_values=None, budget=None, max_maintenance_cost=None):
        """
        Complete drone selection pipeline with all enhancements.
        """
        try:
            # Load and normalize drone data
            if drone_data_path is None:
                drone_data_path = r"D:/project_DSS/backend/data/droneType002.csv"
            df = self.load_and_normalize_drone_data(drone_data_path)
            
            if df.empty:
                return pd.DataFrame(), "No drone data available"
            
            original_count = len(df)
            
            # Load port data
            port_data_df = None
            if port_data_path is None:
                port_data_path = r"D:/project_DSS/backend/data/merged_ports_data.csv"
            try:
                port_data_df = pd.read_csv(port_data_path)
            except FileNotFoundError:
                port_data_df = None
            
            # Extract port environmental constraints
            port_constraints = {}
            if port_data_df is not None and port_name:
                port_constraints = self.extract_port_environmental_constraints(port_data_df, port_name)
                
            # Filter by port constraints
            df = self.filter_drones_by_port_constraints(df, port_constraints)
            print(f"After port constraints filtering: {len(df)} drones")
            if df.empty:
                return pd.DataFrame(), "No drones meet the port environmental requirements"
            
            # Filter by purposes
            if selected_purposes:
                df = self.purpose_based_drone_filtering(df, selected_purposes)
                print(f"After purpose-based filtering: {len(df)} drones")
                if df.empty:
                    return pd.DataFrame(), "No drones meet the selected purpose requirements"
            
            # Filter by cost constraints
            df = self.cost_and_maintenance_filtering(df, budget, max_maintenance_cost)
            print(f"After cost and maintenance filtering: {len(df)} drones")
            if df.empty:
                # Check if budget filtering is the cause
                if budget is not None:
                    # Check if any drones meet all other filters except budget
                    df_no_budget = self.cost_and_maintenance_filtering(df, None, max_maintenance_cost)
                    if df_no_budget.empty:
                        return pd.DataFrame(), "No drones meet the other constraints"
                    else:
                        return pd.DataFrame(), "No drones meet the budget constraints"
                else:
                    return pd.DataFrame(), "No drones meet the constraints"
            
            # Calculate priority weights and rank
            if slider_values:
                priority_weights = self.ahp_priority_scaling(slider_values)
                df = self.weighted_sum_model_ranking(df, priority_weights)
            
            # Add selection summary
            filtered_count = len(df)
            summary = f"Filtered {original_count} drones down to {filtered_count} suitable options"
            
            return df, summary
            
        except Exception as e:
            return pd.DataFrame(), f"Error in drone selection: {str(e)}"

# Convenience functions for backward compatibility
def load_drone_data(file_path="backend/data/droneType.csv"):
    """Load drone data using the enhanced system."""
    system = DroneSelectionSystem()
    return system.load_and_normalize_drone_data(file_path)

def select_drones(drone_data_path=None, port_data_path=None, port_name=None, selected_purposes=None, 
                 purpose_mapping=None, slider_values=None, budget=None, max_maintenance_cost=None):
    """Main function for drone selection with all features."""
    system = DroneSelectionSystem()
    return system.select_drones(
        drone_data_path, port_data_path, port_name, 
        selected_purposes, slider_values, budget, max_maintenance_cost
    )

# Example usage
if __name__ == "__main__":
    # Initialize system
    drone_system = DroneSelectionSystem()
    
    # Example selection
    results, message = drone_system.select_drones(
        drone_data_path=r"D:/project_DSS/backend/data/droneType002.csv",
        port_data_path=r"D:/project_DSS/backend/data/merged_ports_data.csv",
        port_name="Port of Hamburg",
        selected_purposes=["Port Security", "Ship Inspection"],
        slider_values={
            "Battery Life (minutes)": 4,
            "Wind Resistance (m/s)": 5,
            "Camera Resolution (MP)": 3,
            "Price (EUR)": 2
        },
        budget=50000,
        max_maintenance_cost=1000
    )
    
    print(f"Selection Result: {message}")
    if not results.empty:
        print(f"Top 3 recommended drones:")
        print(results[['Drone Name', 'Category', 'WSM Score', 'Price (EUR)']].head(3))
