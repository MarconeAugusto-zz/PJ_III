package pjIII.simova;

import androidx.appcompat.app.AppCompatActivity;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;


public class MainActivity extends AppCompatActivity {

    private Button button_login;
    private EditText email;
    private EditText senha;
    private String username;
    private String password;
    private String ip;
    private String baseUrl;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // TODO: Replace this with your own IP address or URL.
        ip = "192.168.0.14"; //colocar o ip local da máquina poara teste;
        baseUrl = "http://".concat(ip);
        baseUrl = baseUrl.concat(":5000/usuario/login");
        //baseUrl = "http://0.0.0.0:3000";                  //mudar a URL

        email = (EditText) findViewById(R.id.email);
        senha = (EditText) findViewById(R.id.senha);
        button_login = (Button) findViewById(R.id.button);

        button_login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {

                    username = email.getText().toString();
                    password = senha.getText().toString();
                    System.out.println(username);
                    System.out.println(password);

                    ApiAuthenticationClient apiAuthenticationClient =
                            new ApiAuthenticationClient(
                                    baseUrl
                                    , username
                                    , password
                            );

                    AsyncTask<Void, Void, String> execute = new ExecuteNetworkOperation(apiAuthenticationClient);
                    execute.execute();
                } catch (Exception ex) {
                }
            }
        });
    }
    //AsyncTask.e

    @Override
    public void onBackPressed() {
        AlertDialog.Builder builder = new AlertDialog.Builder(this, R.style.Theme_AppCompat_Light_Dialog_Alert);
        builder.setMessage("Deseja realmente sair do aplicativo?")
                .setCancelable(false)
                .setPositiveButton("Sim", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {

                        Intent intent = new Intent(Intent.ACTION_MAIN);
                        intent.addCategory(Intent.CATEGORY_HOME);
                        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                        startActivity(intent);
                        finish();
                    }
                })
                .setNegativeButton("Não", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        dialog.cancel();
                    }
                });
        AlertDialog alert = builder.create();
        alert.show();

    }

    /**
     * Open a new activity window.
     */
    private void goToUserActivity() {

        Toast toast = Toast.makeText(this, "Bem vindo, " + username, Toast.LENGTH_LONG);
        toast.show();
        Intent intent = new Intent(this, UserActivity.class);
        startActivity(intent);

    }

    public class ExecuteNetworkOperation extends AsyncTask<Void, Void, String> {

        private ApiAuthenticationClient apiAuthenticationClient;
        private String isValidCredentials;

        /**
         * Overload the constructor to pass objects to this class.
         */
        public ExecuteNetworkOperation(ApiAuthenticationClient apiAuthenticationClient) {
            this.apiAuthenticationClient = apiAuthenticationClient;
        }

        @Override
        protected String doInBackground(Void... params) {
            try {
                isValidCredentials = apiAuthenticationClient.execute();
            } catch (Exception e) {
                e.printStackTrace();
            }

            return null;
        }

        @Override
        protected void onPostExecute(String result) {
            super.onPostExecute(result);

            // Login Success
            if (isValidCredentials.equals("true")) {
                //goToSecondActivity(); //iniciar a nova activity
                goToUserActivity();
            }
            // Login Failure
            else {
                Toast.makeText(getApplicationContext(), "Falha no login", Toast.LENGTH_LONG).show();
            }
        }
    }
}
