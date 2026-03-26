import pygame, random, sys, json
pygame.init()
screen_info = pygame.display.Info()
width, height = screen_info.current_w, screen_info.current_h
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
FPS = 60
len_list = 100
gap = 2
list_to_sort = [num for num in range(1, len_list+1)]
bar_width = max(1, width // len(list_to_sort))

def load_data():
    global len_list, gap, list_to_sort, bar_width
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
        len_list = data["list length"]
        gap = data["gap between bars"]

        list_to_sort = [num for num in range(1, len_list + 1)]
        bar_width = max(1, width // len_list)
    except FileNotFoundError:
        print("Did not find data.json")
        len_list = 100
        gap = 2

def bubble_sort(data):
    n = len(data)
    for i in range(n):
        for j in range(n - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                yield data

def insertion_sort(data):
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and data[j] > key:
            data[j + 1] = data[j]
            j -= 1
            yield data
        data[j + 1] = key
        yield data

def merge_sort(data, start=0, end=None):
    if end is None: end = len(data)
    if end - start > 1:
        mid = (start + end) // 2
        yield from merge_sort(data, start, mid)
        yield from merge_sort(data, mid, end)
        yield from merge(data, start, mid, end)
        yield data

def merge(data, start, mid, end):
    left = data[start:mid]
    right = data[mid:end]
    i = j = 0

    for k in range(start, end):
        if i >= len(left):
            data[k] = right[j]
            j += 1
        elif j >= len(right):
            data[k] = left[i]
            i += 1
        elif left[i] < right[j]:
            data[k] = left[i]
            i += 1
        else:
            data[k] = right[j]
            j += 1
        yield data

def radix_sort(data):
    max_num = max(data)
    exp = 1
    while max_num // exp > 0:
        buckets = [[] for _ in range(10)]

        for num in data:
            digit = (num // exp) % 10
            buckets[digit].append(num)

        index = 0
        for bucket in buckets:
            for num in bucket:
                data[index] = num
                index += 1
                yield data
        exp *= 10

def selection_sort(data):
    for i in range(len(data)):
        min_idx = i
        for j in range(i, len_list):
            if data[j] < data[min_idx]:
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]
        yield data

def quick_sort(data, low=0, high=None):
    if high is None: high = len(data) - 1
    if low < high:
        pivot_index, updates = yield from partition(data, low, high)
        yield from quick_sort(data, low, pivot_index - 1)
        yield from quick_sort(data, pivot_index + 1, high)
        yield data

def partition(data, low, high):
    pivot = data[high]
    i = low - 1
    updates = []
    for j in range(low, high):
        if data[j] < pivot:
            i += 1
            data[i], data[j] = data[j], data[i]
            updates.append((i, j))
            yield data
    data[i + 1], data[high] = data[high], data[i + 1]
    updates.append((i + 1, high))
    yield data
    return i + 1, updates

def bogo_sort(data):
    def is_sorted(a):
        n = len(a)
        for i in range(0, n-1):
            if a[i] > a[i+1]:
                return False
        return True
    while not is_sorted(data):
        random.shuffle(data)
        yield data

def gnome_sort(data):
    index = 0
    while index < len(data):
        if index == 0 or data[index] >= data[index - 1]:
            index += 1
        else:
            data[index], data[index - 1] = data[index - 1], data[index]
            index -= 1
            yield data

def main() -> None:
    global FPS, screen, len_list, gap, list_to_sort, bar_width, width, height
    load_data()
    clock = pygame.time.Clock()
    sorting = None
    is_sorting = False
    while True:
        pygame.display.set_caption(str(FPS))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                width, height = event.w, event.h
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                bar_width = max(1, width // len(list_to_sort))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RIGHT and FPS < 7680:
                    FPS *= 2
                elif event.key == pygame.K_LEFT and FPS > 15:
                    FPS //= 2
                elif event.key == pygame.K_r and not is_sorting:
                    random.shuffle(list_to_sort)
                elif event.key == pygame.K_1 and not is_sorting:
                    sorting = quick_sort(list_to_sort)
                    is_sorting = True
                elif event.key == pygame.K_2 and not is_sorting:
                    sorting = merge_sort(list_to_sort)
                    is_sorting = True
                elif event.key == pygame.K_3 and not is_sorting:
                    sorting = radix_sort(list_to_sort)
                    is_sorting = True
                elif event.key == pygame.K_4 and not is_sorting:
                    sorting = selection_sort(list_to_sort)
                    is_sorting = True
                elif event.key == pygame.K_5 and not is_sorting:
                    sorting = insertion_sort(list_to_sort)
                    is_sorting = True
                elif event.key == pygame.K_6 and not is_sorting:
                    sorting = bubble_sort(list_to_sort)
                    is_sorting = True
                elif event.key == pygame.K_7 and not is_sorting:
                    sorting = gnome_sort(list_to_sort)
                    is_sorting = True
                elif event.key == pygame.K_8 and not is_sorting:
                    sorting = bogo_sort(list_to_sort)
                    is_sorting = True
        screen.fill(BLACK)
        for idx, value in enumerate(list_to_sort):
            scaled_height = int((value / len_list) * height)
            x = idx * bar_width
            y = height - scaled_height
            pygame.draw.rect(screen, GREEN, (x + gap//2, y, bar_width - gap, scaled_height))
        try:
            next(sorting)
        except StopIteration:
            sorting = None
            is_sorting = False
        except TypeError:
            is_sorting = False
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
