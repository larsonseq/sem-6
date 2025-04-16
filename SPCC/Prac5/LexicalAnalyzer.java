import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

class LexicalAnalyzer {
    public static void main(String[] args) {

        List<String> keywords = new ArrayList<String>();
        List<String> operators = new ArrayList<String>();
        List<String> symbols = new ArrayList<String>();
        List<String> words = new ArrayList<String>();
        Set<String> kSet = new HashSet<String>(); 
        Set<String> iSet = new HashSet<String>(); 
        Set<String> oSet = new HashSet<String>(); 
        Set<String> sSet = new HashSet<String>(); 
        Set<String> lSet = new HashSet<String>(); 

        keywords.addAll(List.of("int", "float", "double", "char", "string", "if", "else", "while", "for", "do",
                "switch", "case", "break", "continue", "return", "void", "main", "class", "public", "static",
                "final", "import", "new", "this", "true", "false", "null"));

        operators.addAll(List.of("=", "+", "-", "*", "/", "%", "++", "--", "&&", "||", "!", "<", ">", "<=", ">="));

        symbols.addAll(List.of("{", "}", "(", ")", "[", "]", ";", ",", "."));

        try {
            FileReader fr = new FileReader("src.txt");
            BufferedReader br = new BufferedReader(fr);
            String line;
            while ((line = br.readLine()) != null) {
                // System.out.println(line);

                for (String word : line.split("\\s+")) {
                    words.add(word);
                }

            }
            br.close();
            fr.close();

        } catch (Exception e) {
            e.printStackTrace();
        }

        for (String word : words) {
            if (keywords.contains(word)) {
              
                    kSet.add(word); 
            } else if (operators.contains(word)) {
                oSet.add(word);
            } else if (symbols.contains(word)) {
                sSet.add(word);
            }else  if (word.matches("\\d+(\\.\\d+)?")) {
                lSet.add(word);
            } 
            else {
                if(!iSet.contains(word)){
                iSet.add(word);
                }
            }
        }
        System.out.println("keywords are :"+kSet+"\noperators are : "+oSet+"\nidentifiers are : "+iSet+"\nsymbols are : "+sSet+"\nliterals are :"+lSet);

        System.out.println("\nSymbol Table:");
        System.out.println("---------------------------");
        System.out.println("Lexeme\t\tToken");
        System.out.println("---------------------------");
        
        java.util.Map<String, Integer> identifierMap = new java.util.HashMap<>();
        int idCounter = 1; 
        
        for (String word : words) {
            String token;
            if (keywords.contains(word)) {
                token = "< " + word + " >";
            } else if (operators.contains(word)) {
                token = "< " + word + " >";
            } else if (symbols.contains(word)) {
                token = "< " + word + " >";
            } else {
                
                if (word.matches("\\d+(\\.\\d+)?")) {
                    token = "< " + word + " >";
                } else {
                    if (!identifierMap.containsKey(word)) {
                        identifierMap.put(word, idCounter++);
                    }
                    token = "<id," + identifierMap.get(word) + ">";
                }
            }
            
            if (word.length() < 8) {
                System.out.println(word + "\t\t" + token);
            } else {
                System.out.println(word + "\t" + token);
            }
        }

    }
}
