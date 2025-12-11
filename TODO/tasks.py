def add_task(tasks):
    task = input('Enter a new task:')
    tasks.append(task)
    print(f'Added: {task}')

def view_tasks(tasks):
    if len(tasks) == 0:
        print('No tasks yet')

    else:
        print('Your Tasks:')
        for i in range(len(tasks)):
            print(f'{i + 1}.{tasks[i]}')

def complete_task(tasks):
    view_tasks(tasks)
    if len(tasks) == 0:
        return
    num = int(input('Enter task number:'))
    if 1 <= num <= len(tasks):
        tasks[num - 1] += ' -> COMPLETED'
        print('Task marked as completed')

    else:
        print('Invalid task number')



def delete_task(tasks):
    view_tasks(tasks)
    if len(tasks) == 0:
        return
    num = int(input('Enter task number : '))
    if 1 <= num <= len(tasks):
        removed = tasks.pop(num-1)
        print('Task removed')

    else:
        print('Invalid task number')
