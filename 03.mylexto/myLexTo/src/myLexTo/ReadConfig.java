/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package myLexTo;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.net.URL;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.json.JSONTokener;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import java.util.Hashtable;

/**
 *
 * @author phisan
 */
public class ReadConfig {

    public Hashtable read() {
        Hashtable config = new Hashtable();

        try {
            File f = new File(System.getProperty("java.class.path"));
            File dir = f.getAbsoluteFile().getParentFile();
            
            String path = dir.getParent().toString();
            String configFile = path+"/config.json";

            JSONTokener jsonTokener = new JSONTokener(new FileReader(path+"/config.json"));
            JSONArray arrobj = new JSONArray(jsonTokener);

            for (int i = 0; i < arrobj.length(); i++) {
                JSONObject item = arrobj.getJSONObject(i);
                String lexitron = item.getString("lexitron");
                String herblist = item.getString("herblist");
                String properties = item.getString("properties");
                String stopwords = item.getString("stopwords");
                String symptoms = item.getString("symptoms");

                config.put("lexitron", lexitron);
                config.put("herblist", herblist);
                config.put("properties", properties);
                config.put("stopwords", stopwords);
                config.put("symptoms", symptoms);
            }
        } catch (FileNotFoundException | JSONException ex) {
            Logger.getLogger(ReadConfig.class.getName()).log(Level.SEVERE, null, ex);
        }

        return config;
    }

    public static void main(String args[]) {
        ReadConfig rconfig = new ReadConfig();
        rconfig.read();
    }
}
