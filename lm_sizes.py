import os
import sys
import multiprocessing
import time

import bf2
import mesher

def worker(jobs, results, modroot):
    while 1:
        next_task = jobs.get()
        if next_task is None:
            jobs.task_done()
            results.put(None)
            break
        filepath = next_task
        try:
            mesh = mesher.LoadBF2Mesh(filepath, loadSamples=True)
            #answer = 'Success loaded samples for {}'.format(filepath)
            meshname = os.path.splitext(os.path.basename(filepath))[0]
            if len(mesh.geoms) == 2: # dest objects
                meshname = ''.join(['DEST:', meshname])
            for geom in mesh.geoms:
                for lod in geom.lod:
                    if lod.sample == None:
                        continue
                    if lod.sample.width == lod.sample.height:
                        meshname = ' '.join([meshname, str(int(lod.sample.width/2))])
                    else:
                        non_iniform_size = '*'.join([str(int(lod.sample.width/2)), str(int(lod.sample.height/2))])
                        meshname = ' '.join([meshname, non_iniform_size])
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
    num_workers = int(multiprocessing.cpu_count()/2)
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
    samples_no_lods = []
    destroyables = []
    no_samples = []
    while 1:
        next_result = results.get()
        if next_result is None:
        #if next_result is False:
            finished_processes += 1
            if finished_processes == len(processes):
                break
        if next_result != None:
            if next_result.startswith('INDEXERROR:'):
                samples_no_lods.append(next_result.replace('INDEXERROR:', ''))
            elif next_result.startswith('DEST:'):
                destroyables.append(next_result.replace('DEST:', ''))
            elif len(next_result.split(' ')) == 1:
                no_samples.append(next_result)
            else:
                print('{}'.format(next_result))
        num_jobs -= 1
    
    # Wait for all of the tasks to finish
    tasks.join()

    # printing special results
    print('[NO_SAMPLES]: {}'.format(len(no_samples)))
    for mesh_no_sample in no_samples:
        print(mesh_no_sample)
    print('[DESTROYABLES]: {}'.format(len(destroyables)))
    for destroyable_result in destroyables:
        print(destroyable_result)
    print('[SAMPLES_NO_LODS]: {}'.format(len(samples_no_lods)))
    for sample_without_lod in samples_no_lods:
        print(sample_without_lod.replace(modroot, ''))

    time_total = time.time() - start_time
    print('Finished parsing {} objects with {} processes in {} seconds'.format(jobs_total, num_workers, time_total))
            
if __name__ == "__main__":
    main(modroot = bf2.Mod().root)
    
