from prometheus_client import start_http_server, REGISTRY, Info, Gauge
import os
import time
import psutil


# Оснонвые метрики для мониторинга
HOST_TYPE = Info('host_type', 'Тип хоста сервера', ['t ype'])
CPU_USAGE = Gauge('cpu_usage_percent', 'Использование CPU в процентах')
MEMORY_USAGE = Gauge('memory_usage_percent', 'Использование RAM в процентах')


def safe_unregister(metric_name):
    """Безопасное удаление лишних питоновских метрик"""
    collector = REGISTRY._names_to_collectors.get(metric_name)
    if collector:
        REGISTRY.unregister(collector)


def get_host_type():
    if os.path.exists('/.dockerenv') or os.environ.get('KUBERNETES_SERVICE_HOST'):
        return 'container'
    
    vm_indicators = [
        '/proc/xen',
        '/sys/hypervisor/uuid',
    ]
    if any(os.path.exists(indicator) for indicator in vm_indicators):
        return 'virtual_machine'
    
    try:
        output = os.popen('systemd-detect-virt').read().strip().lower()
        
        if output == 'none':
            return 'physical_server'
        else:
            return 'virtual_machine'
    except:
        pass
    
    return 'physical_server'


# Обновление статичных метрик - типа хоста
def setup_static_metrics():
    host_type = get_host_type()
    HOST_TYPE.labels(type=host_type)


# Обновление динамических метрик - CPU и RAM
def update_dynamic_metrics():
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.virtual_memory().percent)


safe_unregister('python_gc_objects_collected_total')
safe_unregister('python_info')


if __name__ == '__main__':
    setup_static_metrics()
    start_http_server(8080)
    print("Сервер метрик запущен на http://localhost:8080/metrics")
    
    while True:
        update_dynamic_metrics()
        time.sleep(5)
