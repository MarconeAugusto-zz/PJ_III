package pjIII.simova;


import android.util.Log;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.DataOutputStream;
import java.net.URLEncoder;
import java.util.HashMap;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

/**
 * Created by user on 12/8/17.
 */

public class ApiAuthenticationClient {

    private String baseUrl;
    private String username;
    private String password;
    //private String urlResource;
    private String httpMethod; // GET, POST, PUT, DELETE
    //private String urlPath;
    private String lastResponse;
    private String payload;
    private HashMap<String, String> parameters;
    private Map<String, List<String>> headerFields;

    /**
     *
     * @param baseUrl String
     * @param username String
     * @param password String
     */
    public ApiAuthenticationClient(String  baseUrl, String username, String password) {
        setBaseUrl(baseUrl);
        this.username = username;
        this.password = password;
        this.httpMethod = "POST";
        parameters = new HashMap<>();
        lastResponse = "";
        payload = "";
        headerFields = new HashMap<>();
        // This is important. The application may break without this line.
        System.setProperty("jsse.enableSNIExtension", "false");
    }

    /**
     * --&gt;http://BASE_URL.COM&lt;--/resource/path
     * @param baseUrl the root part of the URL
     * @return this
     */
    public ApiAuthenticationClient setBaseUrl(String baseUrl) {
        this.baseUrl = baseUrl;
        return this;
    }

    /**
     * Get the last response from the Rest API as a JSON Object.
     * @return JSONObject
     */
    public JSONObject getLastResponseAsJsonObject() {
        try {
            return new JSONObject(String.valueOf(lastResponse));
        } catch (JSONException e) {
            e.printStackTrace();
        }
        return null;
    }

    /**
     * Get the last response from the Rest API as a JSON Array.
     * @return JSONArray
     */
    public JSONArray getLastResponseAsJsonArray() {
        try {
            return new JSONArray(String.valueOf(lastResponse));
        } catch (JSONException e) {
            e.printStackTrace();
        }
        return null;
    }

    /**
     * Get the payload as a string from the existing parameters.
     * @return String
     */
    private String getPayloadAsString() {
        // Cycle through the parameters.
        StringBuilder stringBuffer = new StringBuilder();
        Iterator it = parameters.entrySet().iterator();
        int count = 0;
        while (it.hasNext()) {
            Map.Entry pair = (Map.Entry) it.next();
            if (count > 0) {
                stringBuffer.append("&");
            }
            stringBuffer.append(pair.getKey()).append("=").append(pair.getValue());

            it.remove(); // avoids a ConcurrentModificationException
            count++;
        }
        System.out.println("stringBuffer: "+stringBuffer.toString());
        return stringBuffer.toString();
    }

    /**
     * Make the call to the Rest API and return its response as a string.
     * @return String
     */
    public String execute() {
        StringBuilder outputStringBuilder = new StringBuilder();

        try {
            StringBuilder urlString = new StringBuilder(baseUrl);

            URL url = new URL(urlString.toString());

            System.out.println("url: "+url);

            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestProperty("Accept", "application/json");
            connection.setRequestProperty("Content-type", "application/json");
            //connection.setRequestProperty("Content-type", "text/html; charset=UTF-8");
            connection.setRequestMethod("POST");
            connection.setDoInput(true);
            connection.setDoOutput(true);

            JSONObject jsonParam = new JSONObject();
            jsonParam.put("email", username);
            jsonParam.put("senha", password);

            Log.i("JSON", jsonParam.toString());
            DataOutputStream os = new DataOutputStream(connection.getOutputStream());
            os.writeBytes(jsonParam.toString());

            os.flush();
            os.close();

            connection.connect();

            Log.i("STATUS", String.valueOf(connection.getResponseCode()));
            Log.i("MSG" , connection.getResponseMessage());

            if (connection.getResponseCode() == 200){
                return "true";
            }

            connection.disconnect();

        } catch (Exception e) {
            e.printStackTrace();
        }
        return outputStringBuilder.toString();
    }
}