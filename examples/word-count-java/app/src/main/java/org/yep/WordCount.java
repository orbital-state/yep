package org.yep;

import java.io.*;
import java.util.*;
import java.util.regex.*;


public class WordCount {

    public static void main(String[] args) {
        // get the file path from the command line arguments
        // check args length to avoid ArrayIndexOutOfBoundsException
        if (args.length == 0) {
            System.out.println("Please provide a file path as an argument.");
            return;
        }
        String filePath = args[0]; // "declaration.txt";
        List<String> words = readWordsFromFile(filePath);
        List<Map.Entry<String, Integer>> mappedWords = mapWordsToCounts(words);
        Map<String, Integer> wordCounts = reduceWordCounts(mappedWords);
        printWordCounts(wordCounts);
    }

    public static List<String> readWordsFromFile(String filePath) {
        List<String> words = new ArrayList<>();
        try {
            File file = new File(filePath);
            Scanner scanner = new Scanner(file);
            scanner.useDelimiter("\\s+");

            while (scanner.hasNext()) {
                String word = scanner.next();
                // Remove punctuation and convert to lower case
                word = word.replaceAll("[^\\w\\s]", "").toLowerCase();
                if (!word.isEmpty()) {
                    words.add(word);
                }
            }
            scanner.close();
        } catch (FileNotFoundException e) {
            System.out.println("File not found: " + filePath);
            e.printStackTrace();
        }
        return words;
    }

    public static List<Map.Entry<String, Integer>> mapWordsToCounts(List<String> words) {
        Map<String, Integer> wordCounts = new HashMap<>();
        for (String word : words) {
            if (wordCounts.containsKey(word)) {
                wordCounts.put(word, wordCounts.get(word) + 1);
            } else {
                wordCounts.put(word, 1);
            }
        }
        return new ArrayList<>(wordCounts.entrySet());
    }

    public static Map<String, Integer> reduceWordCounts(List<Map.Entry<String, Integer>> mappedWords) {
        Map<String, Integer> wordCounts = new HashMap<>();
        for (Map.Entry<String, Integer> entry : mappedWords) {
            String word = entry.getKey();
            Integer count = entry.getValue();
            wordCounts.put(word, wordCounts.getOrDefault(word, 0) + count);
        }
        return wordCounts;
    }

    public static void printWordCounts(Map<String, Integer> wordCounts) {
        for (Map.Entry<String, Integer> entry : wordCounts.entrySet()) {
            System.out.println(entry.getKey() + ": " + entry.getValue());
        }
    }
}
