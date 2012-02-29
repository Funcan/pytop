from pytop import PyTop
import boto
import euca2ools

def get_instance_count_stat(euca):
    reservations = euca.get_all_instances()
    total = 0
    for reservation in reservations:
    	total += len(reservation.instances)
    return "instances", total

def get_instance_data(euca):
    reservations = euca.get_all_instances()
    ret = []
    for reservation in reservations:
    	for instance in reservation.instances:
    		item = {}
    		item['name'] = instance.displayDescription
    		item['id'] = instance.id
    		item['public_ip'] = instance.ip_address
    		item['ip'] = instance.private_ip_address
    		item['state'] = instance.state
    		ret.append(item)
    return ret

if __name__ == "__main__":
    eucahandle = euca2ools.Euca2ool('ao:x:', compat=True)
    euca = eucahandle.make_connection()

    top = PyTop("euca instance top")
    top.add_stat_source(get_instance_count_stat, euca)
    top.set_data_source(get_instance_data,euca)
    top.run()
