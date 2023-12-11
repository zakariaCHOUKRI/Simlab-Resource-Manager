import json

def parse_sinfo_data(sinfo_output):
    # Example: parse sinfo data for partitions, CPUs, and GPUs
    # This is a placeholder. The actual implementation will depend on the specific format of your sinfo output.
    partitions = []
    for line in sinfo_output.splitlines()[1:]:  # Assuming the first line is a header
        parts = line.split()
        partition_info = {
            'partition': parts[0],
            'CPUs': parts[1],  # Replace with actual index based on your output
            'GPUs': parts[2]   # Replace with actual index based on your output
        }
        partitions.append(partition_info)
    return partitions

def parse_squeue_data(squeue_output):
    # Example: parse squeue data for job details
    # This is a placeholder. The actual implementation will depend on the specific format of your squeue output.
    jobs = []
    for line in squeue_output.splitlines()[1:]:
        parts = line.split()
        job_info = {
            'job_id': parts[0],
            'partition': parts[1],
            'name': parts[2],
            'user': parts[3]
        }
        jobs.append(job_info)
    return jobs

def parse_scontrol_data(scontrol_output):
    # Example: parse scontrol data for node status
    # This is a placeholder. The actual implementation will depend on the specific format of your scontrol output.
    nodes = []
    node_info = {}
    for line in scontrol_output.splitlines():
        if line.startswith('NodeName='):
            if node_info:
                nodes.append(node_info)
            node_info = {'NodeName': line.split('=')[1]}
        elif line:
            key, value = line.split('=', 1)
            node_info[key] = value
    if node_info:
        nodes.append(node_info)
    return nodes

def parse_slurm_data():
    with open('../backend/tmp/sinfo_output.txt', 'r') as file:
        sinfo_data = parse_sinfo_data(file.read())

    with open('../backend/tmp/squeue_output.txt', 'r') as file:
        squeue_data = parse_squeue_data(file.read())

    with open('../backend/tmp/scontrol_output.txt', 'r') as file:
        scontrol_data = parse_scontrol_data(file.read())

    return {
        'sinfo': sinfo_data,
        'squeue': squeue_data,
        'scontrol': scontrol_data
    }

if __name__ == "__main__":
    parsed_data = parse_slurm_data()
    print(json.dumps(parsed_data, indent=4))
