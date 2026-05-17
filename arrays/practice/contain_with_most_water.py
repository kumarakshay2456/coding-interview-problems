def get_containers_with_most_water(height):
    start = 0
    end = len(height) - 1
    max_water = 0
    while start < end:
        min_height = min(height[start], height[end])
        width = end  - start 
        max_water = max(max_water, min_height*width)
        if height[start] < height[end]:
            start += 1
        else:
            end -= 1
    return max_water


def get_total_water(height):
    left = 0
    right = len(height) - 1
    left_max = 0
    right_max = 0
    total_water = 0
    while left < right:
        if height[left] < height[right]:
            if height[left] > left_max:
                left_max = height[left]
            else:
                total_water +=  left_max - height[left]
            left += 1
        else:
            if height[right] > right_max:
                right_max = height[right]
            else:
                total_water +=  right_max - height[right]
            right -= 1
    return total_water





if __name__ == '__main__':
    # height = [0,1,0,2,1,0,1,3,2,1,2,1]
    # print(get_containers_with_most_water(height))


    height = [0,1,0,2,1,0,1,3,2,1,2,1]
    print(get_total_water(height))