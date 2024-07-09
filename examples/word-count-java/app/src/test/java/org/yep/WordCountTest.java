package org.yep;

import org.junit.Test;
import static org.junit.Assert.assertEquals;

import java.util.*;

public class WordCountTest {

    @Test
    public void testMapWordsToCounts() {
        List<String> words = Arrays.asList("test", "test", "word");
        List<Map.Entry<String, Integer>> expected = new ArrayList<>(Map.of("test", 2, "word", 1).entrySet());
        
        // Assuming mapWordsToCounts is made accessible for testing
        List<Map.Entry<String, Integer>> result = WordCount.mapWordsToCounts(words);
        
        assertEquals(new HashSet<>(expected), new HashSet<>(result));
    }

    @Test
    public void testReduceWordCounts() {
        List<Map.Entry<String, Integer>> mappedWords = new ArrayList<>(Map.of("test", 2, "word", 1).entrySet());
        Map<String, Integer> expected = new HashMap<>();
        expected.put("test", 2);
        expected.put("word", 1);
        
        // Assuming reduceWordCounts is made accessible for testing
        Map<String, Integer> result = WordCount.reduceWordCounts(mappedWords);
        
        assertEquals(expected, result);
    }

    // Add more tests here for other methods or edge cases
}