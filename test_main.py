# 这个文件完成测试，不要修改这个文件
import subprocess
import sys
import re

def run_program(input_value):
    """运行学生程序并捕获输出"""
    try:
        process = subprocess.run(
            [sys.executable, "main.py"],
            input=f"{input_value}\n",
            text=True,
            capture_output=True,
            timeout=5
        )
        return process.stdout, process.stderr
    except Exception as e:
        return "", str(e)

def parse_output(output):
    """解析程序输出为结构化数据"""
    results = []
    
    # 解析输出行：年份 地球体重 月球体重
    for line in output.split('\n'):
        if line.strip() and not line.startswith("年份"):
            # 提取数字部分（允许制表符或空格分隔）
            parts = re.findall(r"[\d.]+", line)
            if len(parts) >= 3:
                year = int(parts[0])
                earth_weight = float(parts[1])
                moon_weight = float(parts[2])
                results.append((year, earth_weight, moon_weight))
    
    return results

def test_weight_calculation():
    """主测试函数"""
    test_weight = 50.0  # 测试用起始体重
    stdout, stderr = run_program(test_weight)
    
    if stderr:
        print(f"❌ 程序执行错误: {stderr}")
        exit(1)
    
    output_data = parse_output(stdout)
    
    # 验证输出行数
    if len(output_data) != 10:
        print(f"❌ 输出数据不足10年，只有{len(output_data)}年数据")
        exit(1)
    
    # 验证计算结果
    errors = []
    for year, earth_act, moon_act in output_data:
        # 计算预期值
        earth_exp = test_weight + 0.5 * year
        moon_exp = earth_exp * 0.165
        
        # 允许浮点数精度误差
        earth_diff = abs(earth_act - earth_exp)
        moon_diff = abs(moon_act - moon_exp)
        
        if earth_diff > 0.1:  # 地球体重误差超过0.1kg
            errors.append(f"年份{year}地球体重错误: 应为{earth_exp:.1f}kg, 实际{earth_act:.1f}kg")
        if moon_diff > 0.01:  # 月球体重误差超过0.01kg
            errors.append(f"年份{year}月球体重错误: 应为{moon_exp:.3f}kg, 实际{moon_act:.3f}kg")
    
    if errors:
        for error in errors:
            print(error)
        print(f"❌ 共发现{len(errors)}处错误")
        exit(1)
    else:
        print("✅ 所有测试通过！")
        exit(0)

if __name__ == "__main__":
    test_weight_calculation()
