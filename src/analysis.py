"""
American Express Complaints Analysis Module

This module provides comprehensive analysis of AMEX customer complaints data,
including exploratory data analysis, text analysis, and complaint categorization.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')


class ComplaintsAnalyzer:
    """
    A comprehensive complaints analyzer for AMEX customer complaint data.
    
    This class provides methods for exploratory data analysis, complaint categorization,
    sentiment analysis, and trend identification in customer complaints.
    """
    
    def __init__(self, data: pd.DataFrame = None):
        """
        Initialize the complaints analyzer.
        
        Args:
            data (pd.DataFrame): Complaints dataset. Optional.
        """
        self.data = data
        self.analysis_results = {}
        self.complaint_categories = {
            'billing': ['billing', 'charge', 'payment', 'invoice', 'fee'],
            'service': ['service', 'support', 'response', 'issue', 'resolution'],
            'account': ['account', 'access', 'login', 'security', 'password'],
            'product': ['product', 'offer', 'feature', 'benefits', 'terms'],
            'fraud': ['fraud', 'unauthorized', 'stolen', 'suspicious', 'security breach']
        }
        
    def load_data(self, data: pd.DataFrame) -> None:
        """
        Load complaints data.
        
        Args:
            data (pd.DataFrame): Complaints dataset
        """
        self.data = data
        
    def get_data_overview(self) -> Dict:
        """
        Get an overview of the complaints dataset.
        
        Returns:
            Dict: Overview statistics including shape, missing values, dtypes
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        overview = {
            'total_complaints': len(self.data),
            'total_columns': len(self.data.columns),
            'missing_values': self.data.isnull().sum().to_dict(),
            'data_types': self.data.dtypes.to_dict(),
            'memory_usage_mb': self.data.memory_usage(deep=True).sum() / 1024**2
        }
        
        return overview
    
    def analyze_complaint_volume(self) -> Dict:
        """
        Analyze complaint volume trends over time.
        
        Returns:
            Dict: Complaint volume analysis by period
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        if 'Date' in self.data.columns or 'date' in self.data.columns:
            date_col = 'Date' if 'Date' in self.data.columns else 'date'
            self.data[date_col] = pd.to_datetime(self.data[date_col])
            monthly_volume = self.data.groupby(self.data[date_col].dt.to_period('M')).size()
            
            return {
                'monthly_volume': monthly_volume.to_dict(),
                'total_volume': len(self.data),
                'peak_month': str(monthly_volume.idxmax()) if len(monthly_volume) > 0 else None
            }
        else:
            return {'error': 'Date column not found in data'}
    
    def categorize_complaints(self) -> Dict:
        """
        Categorize complaints based on complaint text/description.
        
        Returns:
            Dict: Complaint categories and their distribution
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        categories = {cat: 0 for cat in self.complaint_categories.keys()}
        category_mapping = []
        
        # Find complaint description column
        desc_col = None
        for col in ['Complaint', 'complaint', 'Description', 'description', 'Issue', 'issue']:
            if col in self.data.columns:
                desc_col = col
                break
        
        if desc_col:
            for idx, complaint in enumerate(self.data[desc_col].fillna('').str.lower()):
                assigned_cat = 'other'
                for category, keywords in self.complaint_categories.items():
                    if any(keyword in complaint for keyword in keywords):
                        assigned_cat = category
                        categories[assigned_cat] += 1
                        break
                
                if assigned_cat == 'other':
                    categories['other'] = categories.get('other', 0) + 1
                
                category_mapping.append(assigned_cat)
            
            self.data['Complaint_Category'] = category_mapping
        
        return categories
    
    def analyze_resolution_time(self) -> Dict:
        """
        Analyze complaint resolution times.
        
        Returns:
            Dict: Resolution time statistics
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        # Look for date columns related to submission and resolution
        resolution_data = {}
        
        date_cols = [col for col in self.data.columns if 'date' in col.lower()]
        
        if len(date_cols) >= 2:
            submitted_col = [col for col in date_cols if 'submit' in col.lower() or 'received' in col.lower()]
            resolved_col = [col for col in date_cols if 'resolve' in col.lower() or 'close' in col.lower()]
            
            if submitted_col and resolved_col:
                self.data[submitted_col[0]] = pd.to_datetime(self.data[submitted_col[0]])
                self.data[resolved_col[0]] = pd.to_datetime(self.data[resolved_col[0]])
                
                resolution_days = (self.data[resolved_col[0]] - self.data[submitted_col[0]]).dt.days
                
                resolution_data = {
                    'mean_resolution_days': resolution_days.mean(),
                    'median_resolution_days': resolution_days.median(),
                    'min_resolution_days': resolution_days.min(),
                    'max_resolution_days': resolution_days.max(),
                    'std_resolution_days': resolution_days.std()
                }
        
        return resolution_data
    
    def get_top_issues(self, n: int = 10) -> List[Tuple[str, int]]:
        """
        Get the top complaint issues.
        
        Args:
            n (int): Number of top issues to return. Default: 10
            
        Returns:
            List[Tuple[str, int]]: Top issues with their counts
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        # Find complaint issue column
        issue_col = None
        for col in ['Sub-issue', 'sub-issue', 'Sub_issue', 'Issue', 'issue']:
            if col in self.data.columns:
                issue_col = col
                break
        
        if issue_col:
            top_issues = self.data[issue_col].value_counts().head(n)
            return list(zip(top_issues.index, top_issues.values))
        
        return []
    
    def generate_summary_report(self) -> Dict:
        """
        Generate a comprehensive summary report of complaints analysis.
        
        Returns:
            Dict: Summary report with all key metrics
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        report = {
            'data_overview': self.get_data_overview(),
            'complaint_volume': self.analyze_complaint_volume(),
            'complaint_categories': self.categorize_complaints(),
            'resolution_time': self.analyze_resolution_time(),
            'top_issues': self.get_top_issues(10)
        }
        
        self.analysis_results = report
        return report
    
    def get_analysis_results(self) -> Dict:
        """
        Get the analysis results from the last report generation.
        
        Returns:
            Dict: Analysis results
        """
        return self.analysis_results
