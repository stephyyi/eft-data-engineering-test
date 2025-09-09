#!/bin/bash
# Setup script for EFT Data Engineering Test Project

set -e  # Exit on error

echo "🚀 Setting up EFT Data Engineering Test Project..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Check MySQL connection
echo "🔌 Checking MySQL connection..."
if ! mysql -u root -e "SELECT 1;" > /dev/null 2>&1; then
    echo "⚠️  MySQL not accessible. Please ensure MySQL is running."
    echo "   On macOS with Homebrew: brew services start mysql"
else
    echo "✅ MySQL is accessible"
    
    # Create analytics database if it doesn't exist
    echo "🗄️  Setting up analytics database..."
    mysql -u root -e "CREATE DATABASE IF NOT EXISTS analytics;"
    echo "✅ Analytics database ready"
fi

# Run tests
echo "🧪 Running setup tests..."
python test_setup.py

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "To get started:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Test data transformation: python src/transform.py --in data/sample_transactions.csv --out output.csv"
echo "3. Run SQL queries in sql/queries.sql against MySQL analytics database"
echo "4. For Airflow (requires additional setup): airflow db init && airflow webserver"
echo ""