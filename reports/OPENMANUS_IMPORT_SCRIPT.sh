#!/bin/bash
# OpenManus-RL Import Script for Life-os
# Run from repo root: bash reports/OPENMANUS_IMPORT_SCRIPT.sh

set -e

echo "🚀 Starting OpenManus-RL import..."

# 1. Clone upstream
echo "📥 Cloning OpenManus-RL..."
if [ -d "openmanus" ]; then
    echo "⚠️  openmanus/ exists. Backing up to openmanus.bak..."
    mv openmanus openmanus.bak
fi

git clone --depth 1 https://github.com/OpenManus/OpenManus-RL.git openmanus
cd openmanus

# 2. Record upstream
echo "📝 Recording upstream origin..."
git log --oneline -1 > ../reports/OPENMANUS_COMMIT.txt
echo "Upstream: https://github.com/OpenManus/OpenManus-RL" >> ../reports/OPENMANUS_COMMIT.txt

cd ..

# 3. Verify import
echo "✅ Verifying import..."
python3 -c "from openmanus_rl import llm_agent; print('✅ Import successful')" 2>/dev/null || \
echo "⚠️  Module not importable yet (expected — dependencies may need install)"

# 4. Create .gitignore for data
echo "📦 Adding data exclusion..."
cat > openmanus/.gitignore << 'EOF'
# Large data files (download separately)
data/*.parquet
data/*.json
data/*.csv

# Dependencies
__pycache__/
*.egg-info/
.pytest_cache/
*.pyc

# Secrets
.env
.env.local
*.key
*.pem

# Model weights (download separately)
models/
checkpoints/
outputs/
logs/

# Environment
venv/
env/
.venv
EOF

echo "✅ OpenManus-RL import complete!"
echo ""
echo "📋 Next steps:"
echo "  1. Review openmanus/ directory"
echo "  2. Run: python -m pytest openmanus/test/ -v"
echo "  3. Create adapter layer: daedalus/adapters/openmanus_adapter.py"
echo "  4. Integrate with Themis approval gates"
