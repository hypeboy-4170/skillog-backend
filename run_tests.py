#!/usr/bin/env python3
import subprocess
import sys
import os

def run_tests():
    """Cognito認証のテストを実行"""
    print("Cognito認証テストを開始...")
    
    try:
        # テスト実行
        result = subprocess.run([
            sys.executable, '-m', 'unittest', 'test_cognito_auth.py', '-v'
        ], capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        print("テスト結果:")
        print(result.stdout)
        
        if result.stderr:
            print("エラー:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ すべてのテストが成功しました")
        else:
            print("❌ テストが失敗しました")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"テスト実行中にエラーが発生しました: {e}")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)