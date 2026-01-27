"""
Monitoring and Analytics System for Weather Wiz
"""
import os
import logging
import psutil
import time
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from models import db, UserAnalytics, AffiliateClick, User, SystemSettings
from sqlalchemy import func, desc
import json

class SystemMonitor:
    """System monitoring and health checks"""
    
    @staticmethod
    def get_system_stats():
        """Get current system statistics"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used = memory.used / (1024**3)  # GB
            memory_total = memory.total / (1024**3)  # GB
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            disk_used = disk.used / (1024**3)  # GB
            disk_total = disk.total / (1024**3)  # GB
            
            # Network stats
            network = psutil.net_io_counters()
            
            return {
                'timestamp': datetime.utcnow().isoformat(),
                'cpu': {
                    'percent': cpu_percent,
                    'count': psutil.cpu_count()
                },
                'memory': {
                    'percent': memory_percent,
                    'used_gb': round(memory_used, 2),
                    'total_gb': round(memory_total, 2)
                },
                'disk': {
                    'percent': round(disk_percent, 2),
                    'used_gb': round(disk_used, 2),
                    'total_gb': round(disk_total, 2)
                },
                'network': {
                    'bytes_sent': network.bytes_sent,
                    'bytes_recv': network.bytes_recv,
                    'packets_sent': network.packets_sent,
                    'packets_recv': network.packets_recv
                }
            }
        except Exception as e:
            logging.error(f"Error getting system stats: {e}")
            return None
    
    @staticmethod
    def check_database_health():
        """Check database connectivity and performance"""
        try:
            start_time = time.time()
            
            # Test basic query
            db.session.execute('SELECT 1')
            
            # Test user count
            user_count = User.query.count()
            
            # Test recent activity
            recent_analytics = UserAnalytics.query.filter(
                UserAnalytics.created_at >= datetime.utcnow() - timedelta(hours=24)
            ).count()
            
            query_time = (time.time() - start_time) * 1000  # ms
            
            return {
                'status': 'healthy',
                'query_time_ms': round(query_time, 2),
                'user_count': user_count,
                'recent_activity_24h': recent_analytics
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e)
            }
    
    @staticmethod
    def get_application_metrics():
        """Get application-specific metrics"""
        try:
            now = datetime.utcnow()
            
            # User metrics
            total_users = User.query.count()
            active_users_24h = UserAnalytics.query.filter(
                UserAnalytics.created_at >= now - timedelta(hours=24)
            ).distinct(UserAnalytics.user_id).count()
            
            premium_users = User.query.filter_by(is_premium=True).count()
            
            # Page view metrics
            page_views_24h = UserAnalytics.query.filter(
                UserAnalytics.event_type == 'page_view',
                UserAnalytics.created_at >= now - timedelta(hours=24)
            ).count()
            
            # Affiliate metrics
            affiliate_clicks_24h = AffiliateClick.query.filter(
                AffiliateClick.created_at >= now - timedelta(hours=24)
            ).count()
            
            conversions_24h = AffiliateClick.query.filter(
                AffiliateClick.converted == True,
                AffiliateClick.created_at >= now - timedelta(hours=24)
            ).count()
            
            # Revenue metrics (if available)
            revenue_24h = db.session.query(
                func.sum(AffiliateClick.conversion_value)
            ).filter(
                AffiliateClick.converted == True,
                AffiliateClick.created_at >= now - timedelta(hours=24)
            ).scalar() or 0
            
            return {
                'users': {
                    'total': total_users,
                    'active_24h': active_users_24h,
                    'premium': premium_users
                },
                'engagement': {
                    'page_views_24h': page_views_24h,
                    'affiliate_clicks_24h': affiliate_clicks_24h,
                    'conversions_24h': conversions_24h
                },
                'revenue': {
                    'revenue_24h': float(revenue_24h)
                }
            }
        except Exception as e:
            logging.error(f"Error getting application metrics: {e}")
            return None

class AnalyticsReporter:
    """Generate analytics reports"""
    
    @staticmethod
    def get_user_analytics(days=7):
        """Get user analytics for specified days"""
        try:
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)
            
            # Daily user activity
            daily_activity = db.session.query(
                func.date(UserAnalytics.created_at).label('date'),
                func.count(func.distinct(UserAnalytics.user_id)).label('active_users'),
                func.count(UserAnalytics.id).label('total_events')
            ).filter(
                UserAnalytics.created_at >= start_date
            ).group_by(
                func.date(UserAnalytics.created_at)
            ).order_by('date').all()
            
            # Top events
            top_events = db.session.query(
                UserAnalytics.event_type,
                func.count(UserAnalytics.id).label('count')
            ).filter(
                UserAnalytics.created_at >= start_date
            ).group_by(
                UserAnalytics.event_type
            ).order_by(desc('count')).limit(10).all()
            
            # User registration trend
            registrations = db.session.query(
                func.date(User.created_at).label('date'),
                func.count(User.id).label('registrations')
            ).filter(
                User.created_at >= start_date
            ).group_by(
                func.date(User.created_at)
            ).order_by('date').all()
            
            return {
                'period': f'{days} days',
                'daily_activity': [
                    {
                        'date': str(row.date),
                        'active_users': row.active_users,
                        'total_events': row.total_events
                    } for row in daily_activity
                ],
                'top_events': [
                    {
                        'event_type': row.event_type,
                        'count': row.count
                    } for row in top_events
                ],
                'registrations': [
                    {
                        'date': str(row.date),
                        'registrations': row.registrations
                    } for row in registrations
                ]
            }
        except Exception as e:
            logging.error(f"Error generating user analytics: {e}")
            return None
    
    @staticmethod
    def get_affiliate_analytics(days=7):
        """Get affiliate marketing analytics"""
        try:
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)
            
            # Daily affiliate performance
            daily_performance = db.session.query(
                func.date(AffiliateClick.created_at).label('date'),
                func.count(AffiliateClick.id).label('clicks'),
                func.count(func.nullif(AffiliateClick.converted, False)).label('conversions'),
                func.sum(AffiliateClick.conversion_value).label('revenue')
            ).filter(
                AffiliateClick.created_at >= start_date
            ).group_by(
                func.date(AffiliateClick.created_at)
            ).order_by('date').all()
            
            # Top products
            top_products = db.session.query(
                AffiliateClick.product_name,
                AffiliateClick.product_brand,
                func.count(AffiliateClick.id).label('clicks'),
                func.count(func.nullif(AffiliateClick.converted, False)).label('conversions'),
                func.sum(AffiliateClick.conversion_value).label('revenue')
            ).filter(
                AffiliateClick.created_at >= start_date
            ).group_by(
                AffiliateClick.product_name,
                AffiliateClick.product_brand
            ).order_by(desc('clicks')).limit(10).all()
            
            # Weather-based performance
            weather_performance = db.session.query(
                AffiliateClick.weather_condition,
                func.count(AffiliateClick.id).label('clicks'),
                func.count(func.nullif(AffiliateClick.converted, False)).label('conversions')
            ).filter(
                AffiliateClick.created_at >= start_date,
                AffiliateClick.weather_condition.isnot(None)
            ).group_by(
                AffiliateClick.weather_condition
            ).order_by(desc('clicks')).all()
            
            return {
                'period': f'{days} days',
                'daily_performance': [
                    {
                        'date': str(row.date),
                        'clicks': row.clicks,
                        'conversions': row.conversions or 0,
                        'revenue': float(row.revenue or 0),
                        'conversion_rate': (row.conversions or 0) / row.clicks * 100 if row.clicks > 0 else 0
                    } for row in daily_performance
                ],
                'top_products': [
                    {
                        'product_name': row.product_name,
                        'product_brand': row.product_brand,
                        'clicks': row.clicks,
                        'conversions': row.conversions or 0,
                        'revenue': float(row.revenue or 0),
                        'conversion_rate': (row.conversions or 0) / row.clicks * 100 if row.clicks > 0 else 0
                    } for row in top_products
                ],
                'weather_performance': [
                    {
                        'weather_condition': row.weather_condition,
                        'clicks': row.clicks,
                        'conversions': row.conversions or 0,
                        'conversion_rate': (row.conversions or 0) / row.clicks * 100 if row.clicks > 0 else 0
                    } for row in weather_performance
                ]
            }
        except Exception as e:
            logging.error(f"Error generating affiliate analytics: {e}")
            return None

class AlertSystem:
    """System for monitoring alerts and notifications"""
    
    ALERT_THRESHOLDS = {
        'cpu_percent': 80,
        'memory_percent': 85,
        'disk_percent': 90,
        'error_rate': 5,  # errors per minute
        'response_time': 2000  # milliseconds
    }
    
    @staticmethod
    def check_system_alerts():
        """Check for system alerts"""
        alerts = []
        
        try:
            stats = SystemMonitor.get_system_stats()
            if not stats:
                alerts.append({
                    'type': 'system',
                    'level': 'critical',
                    'message': 'Unable to retrieve system statistics'
                })
                return alerts
            
            # CPU alert
            if stats['cpu']['percent'] > AlertSystem.ALERT_THRESHOLDS['cpu_percent']:
                alerts.append({
                    'type': 'cpu',
                    'level': 'warning',
                    'message': f"High CPU usage: {stats['cpu']['percent']}%"
                })
            
            # Memory alert
            if stats['memory']['percent'] > AlertSystem.ALERT_THRESHOLDS['memory_percent']:
                alerts.append({
                    'type': 'memory',
                    'level': 'warning',
                    'message': f"High memory usage: {stats['memory']['percent']}%"
                })
            
            # Disk alert
            if stats['disk']['percent'] > AlertSystem.ALERT_THRESHOLDS['disk_percent']:
                alerts.append({
                    'type': 'disk',
                    'level': 'critical',
                    'message': f"High disk usage: {stats['disk']['percent']}%"
                })
            
            return alerts
            
        except Exception as e:
            logging.error(f"Error checking system alerts: {e}")
            return [{
                'type': 'system',
                'level': 'critical',
                'message': f'Error checking alerts: {str(e)}'
            }]
    
    @staticmethod
    def check_application_alerts():
        """Check for application-specific alerts"""
        alerts = []
        
        try:
            # Check database health
            db_health = SystemMonitor.check_database_health()
            if db_health['status'] != 'healthy':
                alerts.append({
                    'type': 'database',
                    'level': 'critical',
                    'message': f"Database unhealthy: {db_health.get('error', 'Unknown error')}"
                })
            
            # Check for recent errors (last 5 minutes)
            recent_errors = UserAnalytics.query.filter(
                UserAnalytics.event_type == 'error',
                UserAnalytics.created_at >= datetime.utcnow() - timedelta(minutes=5)
            ).count()
            
            if recent_errors > AlertSystem.ALERT_THRESHOLDS['error_rate']:
                alerts.append({
                    'type': 'errors',
                    'level': 'warning',
                    'message': f"High error rate: {recent_errors} errors in last 5 minutes"
                })
            
            return alerts
            
        except Exception as e:
            logging.error(f"Error checking application alerts: {e}")
            return [{
                'type': 'application',
                'level': 'critical',
                'message': f'Error checking application alerts: {str(e)}'
            }]

def create_monitoring_blueprint():
    """Create Flask blueprint for monitoring endpoints"""
    from flask import Blueprint
    
    monitoring_bp = Blueprint('monitoring', __name__, url_prefix='/monitoring')
    
    @monitoring_bp.route('/health')
    def health_check():
        """Comprehensive health check endpoint"""
        try:
            system_stats = SystemMonitor.get_system_stats()
            db_health = SystemMonitor.check_database_health()
            app_metrics = SystemMonitor.get_application_metrics()
            
            # Overall health status
            overall_status = 'healthy'
            if not system_stats or db_health['status'] != 'healthy':
                overall_status = 'unhealthy'
            
            return jsonify({
                'status': overall_status,
                'timestamp': datetime.utcnow().isoformat(),
                'system': system_stats,
                'database': db_health,
                'application': app_metrics
            })
        except Exception as e:
            return jsonify({
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }), 500
    
    @monitoring_bp.route('/alerts')
    def get_alerts():
        """Get current system and application alerts"""
        try:
            system_alerts = AlertSystem.check_system_alerts()
            app_alerts = AlertSystem.check_application_alerts()
            
            all_alerts = system_alerts + app_alerts
            
            return jsonify({
                'alerts': all_alerts,
                'count': len(all_alerts),
                'timestamp': datetime.utcnow().isoformat()
            })
        except Exception as e:
            return jsonify({
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }), 500
    
    @monitoring_bp.route('/analytics/users')
    def user_analytics():
        """Get user analytics report"""
        days = request.args.get('days', 7, type=int)
        analytics = AnalyticsReporter.get_user_analytics(days)
        
        if analytics:
            return jsonify(analytics)
        else:
            return jsonify({'error': 'Unable to generate analytics'}), 500
    
    @monitoring_bp.route('/analytics/affiliate')
    def affiliate_analytics():
        """Get affiliate marketing analytics report"""
        days = request.args.get('days', 7, type=int)
        analytics = AnalyticsReporter.get_affiliate_analytics(days)
        
        if analytics:
            return jsonify(analytics)
        else:
            return jsonify({'error': 'Unable to generate analytics'}), 500
    
    return monitoring_bp