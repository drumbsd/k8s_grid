# k8s_grid #

This scripts connect to a k8s/ocp cluster and display a list of all nodes, roles, number of pod running/failed/ etc etc.

## Usage ##

1. Create a virtual env `python3 -m venv ./venv/`
2. `source venv/bin/activate`
3. `pip3 install kubernetes`
4. `pip3 install termcolor`
5. Run it

Example:
```
# python k8s_grid.py --host <host> --token <token>
```

Example output:

![Screenshot](https://user-images.githubusercontent.com/6428880/207646275-40f64b6f-84bf-430c-94b3-cf3d0da0b384.png)
