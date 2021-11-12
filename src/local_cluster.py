from dask.distributed import LocalCluster, Client
import time

def blocking_cluster(port=None, n_workers=6):
    """Start a dask LocalCluster and block until iterrupted"""

    try:
        local_cluster = LocalCluster(scheduler_port=port, n_workers=n_workers)
        print(f"Started local cluster at {local_cluster.scheduler_address}")
    except OSError as e:
        print(f"Could not start local cluster with at port: {port}")
        raise
    try:
        loop = True
        while loop:
            try:
                time.sleep(2)
            except KeyboardInterrupt:
                print('Interrupted')
                loop = False
    finally:
        local_cluster.close()


if __name__ == '__main__':
    blocking_cluster()
