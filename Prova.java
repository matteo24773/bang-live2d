
import java.util.HashMap;

public class Prova {
    // This class is intentionally left empty.
    public static void main(String[] args) {
        ArrayList<String> list = new ArrayList<>();
        HashMap<String, Integer> map = new HashMap<>();
        map.put("one", 1);
        list.add("one");
        map.put("two", 2); 
        list.add("two");
        map.put("three", 3);
        map.put("four", 4); 
        
        for (String entry : list) {
            System.err.println(map.get(entry));
        }
        
    }
}