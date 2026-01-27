#!/usr/bin/env python3
"""
Maintenance and backup utilities for Weather Wiz
"""
import os
import sys
import subprocess
import shutil
import logging
from datetime import datetime, timedelta
from pathlib import Path
import json
import sqlite3
import psycopg2
from models import db, User, UserAnalytics, AffiliateClick, SystemSettings
from app import app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/maintenance.log'),
        logging.StreamHandler()
    ]
)

class BackupManager:
    """Database and file backup management"""
    
    def __init__(self):
        self.backup_dir = Path('backups')
        self.backup_dir.mkdir(exist_ok=True)
        self.max_backups = 30  # Keep 30 days of backups
    
    def create_database_backup(self):
        """Create database backup"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Get database URL
            db_url = os.environ.get('DATABASE_URL', 'sqlite:///weather_wiz.db')
            
            if db_url.startswith('sqlite'):
                # SQLite backup
                db_path = db_url.replace('sqlite:///', '')
                backup_path = self.backup_dir / f'db_backup_{timestamp}.db'
                shutil.copy2(db_path, backup_path)
                logging.info(f"SQLite backup created: {backup_path}")
                
            elif db_url.startswith('postgresql'):
                # PostgreSQL backup
                backup_path = self.backup_dir / f'db_backup_{timestamp}.sql'
                
                # Extract connection details
                import urllib.parse as urlparse
                parsed = urlparse.urlparse(db_url)
                
                env = os.environ.copy()
                env['PGPASSWORD'] = parsed.password
                
                cmd = [
                    'pg_dump',
                    '-h', parsed.hostname,
                    '-p', str(parsed.port or 5432),
                    '-U', parsed.username,
                    '-d', parsed.path[1:],  # Remove leading slash
                    '-f', str(backup_path)
                ]
                
                result = subprocess.run(cmd, env=env, capture_output=True, text=True)
                
                if result.returncode == 0:
                    logging.info(f"PostgreSQL backup created: {backup_path}")
                else:
                    logging.error(f"PostgreSQL backup failed: {result.stderr}")
                    return False
            
            return True
            
        except Exception as e:
            logging.error(f"Database backup failed: {e}")
            return False
    
    def create_files_backup(self):
        """Create backup of uploaded files and logs"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Backup uploads directory
            if os.path.exists('uploads'):
                backup_path = self.backup_dir / f'uploads_backup_{timestamp}.tar.gz'
                subprocess.run([
                    'tar', '-czf', str(backup_path), 'uploads/'
                ], check=True)
                logging.info(f"Files backup created: {backup_path}")
            
            # Backup logs directory
            if os.path.exists('logs'):
                backup_path = self.backup_dir / f'logs_backup_{timestamp}.tar.gz'
                subprocess.run([
                    'tar', '-czf', str(backup_path), 'logs/'
                ], check=True)
                logging.info(f"Logs backup created: {backup_path}")
            
            return True
            
        except Exception as e:
            logging.error(f"Files backup failed: {e}")
            return False
    
    def cleanup_old_backups(self):
        """Remove old backup files"""
        try:
            cutoff_date = datetime.now() - timedelta(days=self.max_backups)
            
            for backup_file in self.backup_dir.glob('*'):
                if backup_file.is_file():
                    file_time = datetime.fromtimestamp(backup_file.stat().st_mtime)
                    if file_time < cutoff_date:
                        backup_file.unlink()
                        logging.info(f"Removed old backup: {backup_file}")
            
            return True
            
        except Exception as e:
            logging.error(f"Backup cleanup failed: {e}")
            return False
    
    def restore_database(self, backup_file):
        """Restore database from backup"""
        try:
            backup_path = Path(backup_file)
            if not backup_path.exists():
                logging.error(f"Backup file not found: {backup_file}")
                return False
            
            db_url = os.environ.get('DATABASE_URL', 'sqlite:///weather_wiz.db')
            
            if db_url.startswith('sqlite') and backup_path.suffix == '.db':
                # SQLite restore
                db_path = db_url.replace('sqlite:///', '')
                shutil.copy2(backup_path, db_path)
                logging.info(f"SQLite database restored from: {backup_path}")
                
            elif db_url.startswith('postgresql') and backup_path.suffix == '.sql':
                # PostgreSQL restore
                import urllib.parse as urlparse
                parsed = urlparse.urlparse(db_url)
                
                env = os.environ.copy()
                env['PGPASSWORD'] = parsed.password
                
                cmd = [
                    'psql',
                    '-h', parsed.hostname,
                    '-p', str(parsed.port or 5432),
                    '-U', parsed.username,
                    '-d', parsed.path[1:],
                    '-f', str(backup_path)
                ]
                
                result = subprocess.run(cmd, env=env, capture_output=True, text=True)
                
                if result.returncode == 0:
                    logging.info(f"PostgreSQL database restored from: {backup_path}")
                else:
                    logging.error(f"PostgreSQL restore failed: {result.stderr}")
                    return False
            
            return True
            
        except Exception as e:
            logging.error(f"Database restore failed: {e}")
            return False

class DataCleaner:
    """Clean up old data and optimize database"""
    
    def __init__(self):
        self.retention_days = {
            'analytics': 90,  # Keep analytics for 90 days
            'affiliate_clicks': 365,  # Keep affiliate data for 1 year
            'logs': 30  # Keep log files for 30 days
        }
    
    def cleanup_analytics_data(self):
        """Remove old analytics data"""
        try:
            with app.app_context():
                cutoff_date = datetime.utcnow() - timedelta(days=self.retention_days['analytics'])
                
                # Delete old analytics records
                deleted = UserAnalytics.query.filter(
                    UserAnalytics.created_at < cutoff_date
                ).delete()
                
                db.session.commit()
                logging.info(f"Deleted {deleted} old analytics records")
                
            return True
            
        except Exception as e:
            logging.error(f"Analytics cleanup failed: {e}")
            return False
    
    def cleanup_affiliate_data(self):
        """Remove old affiliate click data (keep conversions)"""
        try:
            with app.app_context():
                cutoff_date = datetime.utcnow() - timedelta(days=self.retention_days['affiliate_clicks'])
                
                # Delete old non-converted clicks
                deleted = AffiliateClick.query.filter(
                    AffiliateClick.created_at < cutoff_date,
                    AffiliateClick.converted == False
                ).delete()
                
                db.session.commit()
                logging.info(f"Deleted {deleted} old affiliate click records")
                
            return True
            
        except Exception as e:
            logging.error(f"Affiliate data cleanup failed: {e}")
            return False
    
    def cleanup_log_files(self):
        """Remove old log files"""
        try:
            if not os.path.exists('logs'):
                return True
            
            cutoff_date = datetime.now() - timedelta(days=self.retention_days['logs'])
            
            for log_file in Path('logs').glob('*.log*'):
                if log_file.is_file():
                    file_time = datetime.fromtimestamp(log_file.stat().st_mtime)
                    if file_time < cutoff_date:
                        log_file.unlink()
                        logging.info(f"Removed old log file: {log_file}")
            
            return True
            
        except Exception as e:
            logging.error(f"Log cleanup failed: {e}")
            return False
    
    def optimize_database(self):
        """Optimize database performance"""
        try:
            with app.app_context():
                db_url = os.environ.get('DATABASE_URL', 'sqlite:///weather_wiz.db')
                
                if db_url.startswith('sqlite'):
                    # SQLite optimization
                    db.session.execute('VACUUM')
                    db.session.execute('ANALYZE')
                    logging.info("SQLite database optimized")
                    
                elif db_url.startswith('postgresql'):
                    # PostgreSQL optimization
                    db.session.execute('VACUUM ANALYZE')
                    logging.info("PostgreSQL database optimized")
                
                db.session.commit()
                
            return True
            
        except Exception as e:
            logging.error(f"Database optimization failed: {e}")
            return False

class SystemMaintenance:
    """System maintenance tasks"""
    
    def __init__(self):
        self.backup_manager = BackupManager()
        self.data_cleaner = DataCleaner()
    
    def run_daily_maintenance(self):
        """Run daily maintenance tasks"""
        logging.info("Starting daily maintenance...")
        
        tasks = [
            ("Database backup", self.backup_manager.create_database_backup),
            ("Files backup", self.backup_manager.create_files_backup),
            ("Cleanup old backups", self.backup_manager.cleanup_old_backups),
            ("Cleanup analytics data", self.data_cleaner.cleanup_analytics_data),
            ("Cleanup log files", self.data_cleaner.cleanup_log_files),
        ]
        
        results = {}
        for task_name, task_func in tasks:
            try:
                logging.info(f"Running: {task_name}")
                results[task_name] = task_func()
            except Exception as e:
                logging.error(f"Task failed - {task_name}: {e}")
                results[task_name] = False
        
        # Log summary
        successful = sum(1 for success in results.values() if success)
        total = len(results)
        logging.info(f"Daily maintenance completed: {successful}/{total} tasks successful")
        
        return results
    
    def run_weekly_maintenance(self):
        """Run weekly maintenance tasks"""
        logging.info("Starting weekly maintenance...")
        
        tasks = [
            ("Cleanup affiliate data", self.data_cleaner.cleanup_affiliate_data),
            ("Optimize database", self.data_cleaner.optimize_database),
        ]
        
        results = {}
        for task_name, task_func in tasks:
            try:
                logging.info(f"Running: {task_name}")
                results[task_name] = task_func()
            except Exception as e:
                logging.error(f"Task failed - {task_name}: {e}")
                results[task_name] = False
        
        # Log summary
        successful = sum(1 for success in results.values() if success)
        total = len(results)
        logging.info(f"Weekly maintenance completed: {successful}/{total} tasks successful")
        
        return results
    
    def generate_system_report(self):
        """Generate system health and usage report"""
        try:
            with app.app_context():
                report = {
                    'timestamp': datetime.utcnow().isoformat(),
                    'database': {
                        'total_users': User.query.count(),
                        'active_users_7d': UserAnalytics.query.filter(
                            UserAnalytics.created_at >= datetime.utcnow() - timedelta(days=7)
                        ).distinct(UserAnalytics.user_id).count(),
                        'total_analytics_records': UserAnalytics.query.count(),
                        'total_affiliate_clicks': AffiliateClick.query.count(),
                    },
                    'system': {
                        'backup_count': len(list(Path('backups').glob('*'))),
                        'log_files': len(list(Path('logs').glob('*.log*'))) if os.path.exists('logs') else 0,
                        'upload_files': len(list(Path('uploads').glob('*'))) if os.path.exists('uploads') else 0,
                    }
                }
                
                # Save report
                report_path = Path('logs') / f'system_report_{datetime.now().strftime("%Y%m%d")}.json'
                report_path.parent.mkdir(exist_ok=True)
                
                with open(report_path, 'w') as f:
                    json.dump(report, f, indent=2)
                
                logging.info(f"System report generated: {report_path}")
                return report
                
        except Exception as e:
            logging.error(f"System report generation failed: {e}")
            return None

def main():
    """Main maintenance script"""
    if len(sys.argv) < 2:
        print("Usage: python maintenance.py <command>")
        print("Commands:")
        print("  daily     - Run daily maintenance tasks")
        print("  weekly    - Run weekly maintenance tasks")
        print("  backup    - Create database and files backup")
        print("  cleanup   - Clean up old data")
        print("  report    - Generate system report")
        print("  restore   - Restore database from backup file")
        sys.exit(1)
    
    command = sys.argv[1]
    maintenance = SystemMaintenance()
    
    if command == 'daily':
        maintenance.run_daily_maintenance()
    elif command == 'weekly':
        maintenance.run_weekly_maintenance()
    elif command == 'backup':
        maintenance.backup_manager.create_database_backup()
        maintenance.backup_manager.create_files_backup()
    elif command == 'cleanup':
        maintenance.data_cleaner.cleanup_analytics_data()
        maintenance.data_cleaner.cleanup_affiliate_data()
        maintenance.data_cleaner.cleanup_log_files()
    elif command == 'report':
        report = maintenance.generate_system_report()
        if report:
            print(json.dumps(report, indent=2))
    elif command == 'restore':
        if len(sys.argv) < 3:
            print("Usage: python maintenance.py restore <backup_file>")
            sys.exit(1)
        maintenance.backup_manager.restore_database(sys.argv[2])
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()