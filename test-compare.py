import subprocess
import time
import os
import signal

def run_test(server_type, num_runs=5):
    times = []
    for i in range(num_runs):
        if server_type == 'single':
            proc = subprocess.Popen(['python3', 'server.py'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(1)
            result = subprocess.run(['python3', 'client-timed.py', '--single'], capture_output=True, text=True)
        else:
            proc = subprocess.Popen(['python3', 'server-mult.py'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(1)
            result = subprocess.run(['python3', 'client-timed.py', '--multi'], capture_output=True, text=True)
        
        output = result.stdout.strip()
        if 'Tempo total:' in output:
            time_str = output.split('Tempo total:')[1].split('s')[0].strip()
            times.append(float(time_str))
        
        proc.terminate()
        proc.wait()
        time.sleep(1)
    
    return times

print("=== Teste Single-Thread ===")
single_times = run_test('single', 5)
print(f"Tempos: {single_times}")
print(f"Média: {sum(single_times)/len(single_times):.4f}s")

print("\n=== Teste Multi-Thread ===")
multi_times = run_test('multi', 5)
print(f"Tempos: {multi_times}")
print(f"Média: {sum(multi_times)/len(multi_times):.4f}s")

print("\n=== Comparação ===")
print(f"Single-Thread médio: {sum(single_times)/len(single_times):.4f}s")
print(f"Multi-Thread médio: {sum(multi_times)/len(multi_times):.4f}s")