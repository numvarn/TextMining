/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package myLexTo;

import LexTo.LongLexTo;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Hashtable;
import java.util.Vector;

/**
 *
 * @author phisan
 */
public class myLexTo {
    
    private static Hashtable config = new Hashtable();
    
    public static void main(String args[]) throws IOException {
        if (args.length > 0) {
            /* Read Config File*/
            ReadConfig rconfig = new ReadConfig();
            config = rconfig.read();
            
            String baseDirectory = args[0];
            String targetDirectory = baseDirectory + "/lexto";
            String textDirectory = targetDirectory + "/text";
            String htmlDirectory = targetDirectory + "/html";
            String line;
            
            int begin, end, type;
            String [] nameTokens;

            File inFile, outFile, outFileHTML;
            FileReader fr;
            BufferedReader br;
            FileWriter fw, fwhtml;
            Vector typeList;

            File theDir = new File(targetDirectory);
            if (!theDir.exists()) {
                try {
                    theDir.mkdir();
                } catch (SecurityException se) {
                    System.out.println(se);
                }
            }

            File textDir = new File(textDirectory);
            if (!textDir.exists()) {
                try {
                    textDir.mkdir();
                } catch (SecurityException se) {
                    System.out.println(se);
                }
            }

            File htmlDir = new File(htmlDirectory);
            if (!htmlDir.exists()) {
                try {
                    htmlDir.mkdir();
                } catch (SecurityException se) {
                    System.out.println(se);
                }
            }

            /* Create LexTo instance*/
            LongLexTo tokenizer = new LongLexTo(new File((String) config.get("lexitron")));
            File herblist = new File((String) config.get("herblist"));
            File properties = new File((String) config.get("properties"));
            File stopwords = new File((String) config.get("stopwords"));
            File symptoms = new File((String) config.get("symptoms"));
            
            if (herblist.exists()) {
                tokenizer.addDict(herblist);
            }else {
                System.out.println("Herb name list is not exits !!");
                System.exit(0);
            }
            
            if (properties.exists()) {
                tokenizer.addDict(properties);
            } else {
                System.out.println("Properties list is not exitst !!");
                System.exit(0);
            }
            
            if (stopwords.exists()) {
                tokenizer.addDict(stopwords);
            } else {
                System.out.println("Stop words list is not exitst !!");
                System.exit(0);
            }
            
            if (symptoms.exists()) {
                tokenizer.addDict(symptoms);
            } else {
                System.out.println("Stop words list is not exitst !!");
                System.exit(0);
            }

            final File folder = new File(baseDirectory);
            int count = 1;
            for (final File fileEntry : folder.listFiles()) {
                if (!fileEntry.isDirectory()) {
                    System.out.println(count + " : Processed File -- " + fileEntry.getName());
                    
                    nameTokens = fileEntry.getName().split("\\.(?=[^\\.]+$)");
                    
                    inFile = new File(baseDirectory + "//" + fileEntry.getName());
                    outFile = new File(textDirectory + "//" + fileEntry.getName());
                    outFileHTML = new File(htmlDirectory + "//" + nameTokens[0]+".html");

                    fr = new FileReader(inFile);
                    br = new BufferedReader(fr);
                    fw = new FileWriter(outFile);
                    fwhtml = new FileWriter(outFileHTML);

                    while ((line = br.readLine()) != null) {
                        line = line.trim();
                        if (line.length() > 0) {
                            tokenizer.wordInstance(line);
                            typeList = tokenizer.getTypeList();
                            
                            begin = tokenizer.first();
                            int i = 0;
                            while (tokenizer.hasNext()) {
                                end = tokenizer.next();
                                
                                /* write to Text file */
                                fw.write(line.substring(begin, end));
                                fw.write("|");

                                /* write HTML file*/
                                type = ((Integer) typeList.elementAt(i++)).intValue();
                                if (type == 0) {
                                    fwhtml.write("<font color=#ff0000>" + line.substring(begin, end) + "</font>");
                                } else if (type == 1) {
                                    fwhtml.write("<font color=#00bb00>" + line.substring(begin, end) + "</font>");
                                } else if (type == 2) {
                                    fwhtml.write("<font color=#0000bb>" + line.substring(begin, end) + "</font>");
                                } else if (type == 3) {
                                    fwhtml.write("<font color=#aa00aa>" + line.substring(begin, end) + "</font>");
                                } else if (type == 4) {
                                    fwhtml.write("<font color=#00aaaa>" + line.substring(begin, end) + "</font>");
                                }
                                fwhtml.write("<font color=#000000>|</font>");
                                
                                begin = end;
                            }
                            fw.write(System.lineSeparator());
                            fw.write(System.lineSeparator());
                            
                            fwhtml.write("<br>\n");
                        }
                    }

                    fr.close();
                    fw.close();
                    fwhtml.close();
                    count++;
                }
            }
        } else {
            System.out.println("Please, Enter file path.");
            System.exit(0);
        }
    }
}
