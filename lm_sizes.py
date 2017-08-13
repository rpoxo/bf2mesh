import os
import sys
import multiprocessing
import time

import bf2
import modmesh

def worker(jobs, results, modroot):
    while 1:
        next_task = jobs.get()
        if next_task is None:
            jobs.task_done()
            results.put(None)
            break
        filepath = next_task
        try:
            mesh = modmesh.LoadBF2Mesh(filepath, loadSamples=True)
            #answer = 'Success loaded samples for {}'.format(filepath)
            meshname = os.path.splitext(os.path.basename(filepath))[0]
            if len(mesh.geoms) == 2: # dest objects
                meshname = ''.join(['DEST:', meshname])
            for geom in mesh.geoms:
                for lod in geom.lods:
                    if lod.sample == None:
                        continue
                    if lod.sample.width == lod.sample.height:
                        meshname = ' '.join([meshname, str(int(lod.sample.width/2))])
                    else:
                        non_iniform_size = '*'.join([str(int(lod.sample.width/2)), str(int(lod.sample.height/2))])
                        meshname = ' '.join([meshname, non_iniform_size])
                    if lod.sample.width == 0 or lod.sample.height == 0:
                        meshname = ''.join(['ZERO:', meshname])
            answer = meshname
            # freeing memory lol
            del mesh
            del next_task
            del meshname
        except IndexError:
            answer = 'INDEXERROR:{}'.format(filepath)
        jobs.task_done()
        results.put(answer)
        # freeing memory lol
        del filepath
        del answer
            


def main(modroot):
    start_time = time.time()

    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()

    # initializing workers
    processes = []
    num_workers = int(multiprocessing.cpu_count())
    for i in range(num_workers):
        proc = multiprocessing.Process(target=worker, args=(tasks, results, modroot,))
        proc.start()
        processes.append(proc)

    # walking over dirs and sending filepath
    num_jobs = 0
    scanpath = os.path.join(modroot, 'objects', 'staticobjects')
    for dir, dirnames, filenames in os.walk(scanpath):
        for filename in filenames:
            filepath = os.path.join(scanpath, dir, filename)
            name = os.path.splitext(filename)[0]
            ext = os.path.splitext(filename)[1]
            if ext == '.staticmesh':
                tasks.put(filepath)
                num_jobs += 1
                #print('ADD:[{}]\n{}'.format(num_jobs, filepath))
    jobs_total = int(num_jobs)
    
    # adding poison pill
    for process in processes:
        tasks.put(None)
    #print('added poisong pill')

    # Start parsing results
    finished_processes = 0
    lm_data = {
        'nolods' : [],
        'dest' : [],
        'nosamp' : [],
        'zeroed' : [],
        'valid' : [],
        }
    while 1:
        next_result = results.get()
        if next_result is None:
        #if next_result is False:
            finished_processes += 1
            if finished_processes == len(processes):
                break
        if next_result != None:
            if next_result.startswith('INDEXERROR:'):
                lm_data['nolods'].append(next_result.replace('INDEXERROR:', ''))
            elif next_result.startswith('DEST:'):
                lm_data['dest'].append(next_result.replace('DEST:', ''))
            elif next_result.startswith('ZERO:'):
                lm_data['zeroed'].append(next_result.replace('ZERO:', ''))
            elif len(next_result.split(' ')) == 1:
                lm_data['nosamp'].append(next_result)
            else:
                lm_data['valid'].append(next_result)
        num_jobs -= 1
    
    # Wait for all of the tasks to finish
    tasks.join()

    # printing results
    lm_data['valid'].sort()
    print('[VALID]: {}'.format(len(lm_data['valid'])))
    for mesh_with_sample in lm_data['valid']:
        print(mesh_with_sample)
    
    lm_data['nosamp'].sort()
    print('[NO_SAMPLES]: {}'.format(len(lm_data['nosamp'])))
    for mesh_no_sample in lm_data['nosamp']:
        print(mesh_no_sample)
    
    lm_data['dest'].sort()
    print('[DESTROYABLES]: {}'.format(len(lm_data['dest'])))
    for destroyable_result in lm_data['dest']:
        print(destroyable_result)
    
    lm_data['zeroed'].sort()
    print('[INVALID_ZEROED]: {}'.format(len(lm_data['zeroed'])))
    for zeroed_sample in lm_data['zeroed']:
        print(zeroed_sample)
        
    lm_data['nolods'].sort()
    print('[SAMPLES_NO_LODS]: {}'.format(len(lm_data['nolods'])))
    for sample_without_lod in lm_data['nolods']:
        print(sample_without_lod.replace(modroot, ''))

    time_total = time.time() - start_time
    print('Finished parsing {} objects with {} processes in {} seconds'.format(jobs_total, num_workers, time_total))
            
if __name__ == "__main__":
    main(modroot = bf2.Mod().root)
    
