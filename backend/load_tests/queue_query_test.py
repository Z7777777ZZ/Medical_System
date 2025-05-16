#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
患者队列状态查询性能测试脚本 - 模拟100个并发请求
测试API: /api/users/patients/queue_status
"""

import requests
import time
import json
import concurrent.futures
import statistics
import argparse
from datetime import datetime

# 配置
DEFAULT_BASE_URL = "http://localhost:5000"  # 默认后端服务地址
DEFAULT_CONCURRENCY = 100  # 默认并发数
DEFAULT_TEST_DURATION = 60  # 默认测试时长(秒)
DEFAULT_ITERATIONS = 1  # 默认测试轮次

# 测试指标
class MetricsCollector:
    def __init__(self):
        self.response_times = []
        self.status_codes = {}
        self.successful_requests = 0
        self.failed_requests = 0
        self.start_time = None
        self.end_time = None
    
    def start_test(self):
        self.start_time = time.time()
    
    def end_test(self):
        self.end_time = time.time()
    
    def add_result(self, response_time, status_code, is_success):
        self.response_times.append(response_time)
        
        # 记录状态码分布
        if status_code in self.status_codes:
            self.status_codes[status_code] += 1
        else:
            self.status_codes[status_code] = 1
        
        # 记录成功/失败请求
        if is_success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1
    
    def get_summary(self):
        if not self.response_times:
            return "没有请求被执行"
        
        total_duration = self.end_time - self.start_time
        requests_per_second = (self.successful_requests + self.failed_requests) / total_duration
        
        # 计算响应时间统计数据
        avg_response_time = statistics.mean(self.response_times) if self.response_times else 0
        min_response_time = min(self.response_times) if self.response_times else 0
        max_response_time = max(self.response_times) if self.response_times else 0
        
        # 如果有足够的样本，计算95%和99%分位数
        percentile_95 = 0
        percentile_99 = 0
        if len(self.response_times) > 10:
            sorted_times = sorted(self.response_times)
            idx_95 = int(len(sorted_times) * 0.95)
            idx_99 = int(len(sorted_times) * 0.99)
            percentile_95 = sorted_times[idx_95]
            percentile_99 = sorted_times[idx_99]
        
        # 生成摘要
        summary = {
            "测试时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "总请求数": self.successful_requests + self.failed_requests,
            "成功请求": self.successful_requests,
            "失败请求": self.failed_requests,
            "总测试时间(秒)": round(total_duration, 2),
            "每秒请求数(RPS)": round(requests_per_second, 2),
            "响应时间(秒)": {
                "平均": round(avg_response_time, 3),
                "最小": round(min_response_time, 3),
                "最大": round(max_response_time, 3),
                "95%分位数": round(percentile_95, 3),
                "99%分位数": round(percentile_99, 3),
            },
            "状态码分布": self.status_codes
        }
        
        return summary

def get_queue_status(base_url, patient_id=None):
    """执行队列状态查询"""
    url = f"{base_url}/api/users/patients/queue_status"
    headers = {}
    
    # 如果有患者ID，添加JWT令牌（在实际测试中需要通过登录获取）
    if patient_id:
        # 在真实测试中，这里应该使用实际的JWT令牌
        headers["Authorization"] = f"Bearer {patient_id}"
    
    start_time = time.time()
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response_time = time.time() - start_time
        
        return {
            "response_time": response_time,
            "status_code": response.status_code,
            "is_success": response.status_code == 200,
            "data": response.json() if response.status_code == 200 else None
        }
    except Exception as e:
        response_time = time.time() - start_time
        return {
            "response_time": response_time,
            "status_code": 0,
            "is_success": False,
            "error": str(e)
        }

def worker(base_url, metrics, patient_id=None):
    """工作线程函数，执行单次请求"""
    result = get_queue_status(base_url, patient_id)
    metrics.add_result(
        result["response_time"], 
        result["status_code"],
        result["is_success"]
    )
    return result

def run_load_test(base_url, concurrency, duration, iterations):
    """运行负载测试"""
    print(f"开始队列查询负载测试 - {concurrency}个并发请求，持续{duration}秒，{iterations}轮次")
    
    all_metrics = []
    
    for i in range(iterations):
        print(f"\n正在执行第{i+1}轮测试...")
        
        # 创建指标收集器
        metrics = MetricsCollector()
        metrics.start_test()
        
        # 记录开始时间
        start_time = time.time()
        end_time = start_time + duration
          # 使用线程池执行并发请求
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
            # 提交请求任务，直到达到指定的测试持续时间
            futures = []
            request_count = 0
            
            while time.time() < end_time:
                # 模拟不同患者ID (在实际应用中，我们需要有有效的JWT令牌)
                # 这里我们不传递patient_id，因为这个API端点可能不需要认证就能访问
                # 如果需要认证，则需要先登录获取JWT令牌
                futures.append(
                    executor.submit(worker, base_url, metrics)
                )
                request_count += 1
                
                # 控制提交速率，避免过快提交任务
                if len(futures) % concurrency == 0:
                    time.sleep(0.1)
            
            # 等待所有任务完成
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"任务执行出错: {e}")
        
        # 计算最终指标
        metrics.end_test()
        summary = metrics.get_summary()
        all_metrics.append(summary)
        
        # 输出本轮测试结果
        print(f"第{i+1}轮测试完成:")
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    
    # 输出所有轮次的平均结果
    if iterations > 1:
        print("\n所有测试轮次的平均结果:")
        avg_rps = statistics.mean([m["每秒请求数(RPS)"] for m in all_metrics])
        avg_resp_time = statistics.mean([m["响应时间(秒)"]["平均"] for m in all_metrics])
        print(f"平均每秒请求数(RPS): {round(avg_rps, 2)}")
        print(f"平均响应时间(秒): {round(avg_resp_time, 3)}")
    
    return all_metrics

def main():
    parser = argparse.ArgumentParser(description="队列查询负载测试工具")
    parser.add_argument("--url", default=DEFAULT_BASE_URL, help="后端API基础URL")
    parser.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY, help="并发连接数")
    parser.add_argument("--duration", type=int, default=DEFAULT_TEST_DURATION, help="测试持续时间(秒)")
    parser.add_argument("--iterations", type=int, default=DEFAULT_ITERATIONS, help="测试轮次")
    args = parser.parse_args()
    
    # 运行负载测试
    try:
        run_load_test(args.url, args.concurrency, args.duration, args.iterations)
    except KeyboardInterrupt:
        print("\n测试被用户中断")
    except Exception as e:
        print(f"\n测试失败: {e}")

if __name__ == "__main__":
    main()
