import java.util.*;

public class Main {

    public static int getMaxLengthOptimized(int[] nums) {
        int prefixSum = 0;
        int maxLength = 0;

        Map<Integer, Integer> firstOccurrence = new HashMap<>();
        firstOccurrence.put(0, -1);

        for (int i = 0; i < nums.length; i++) {
            prefixSum += (nums[i] == 1) ? 1 : -1;

            if (firstOccurrence.containsKey(prefixSum)) {
                maxLength = Math.max(maxLength, i - firstOccurrence.get(prefixSum));
            } else {
                firstOccurrence.put(prefixSum, i);
            }
        }

        return maxLength;
    }

    public static void main(String[] args) {
        int[] nums = {0, 1};
        System.out.println(getMaxLengthOptimized(nums));
    }
}