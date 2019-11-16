package pjIII.simova;

import java.util.List;

public class User {


    private static String Nome;
    private static String token;
    public static List<String> vagas;
    public static List<String> eventos;


    public static String getEventos(int pos) {
        if (eventos.get(pos)!= null){
            return eventos.get(pos);
        }else
            return null;
    }

    public static void setEventos(List<String> eventos) {
        User.eventos = eventos;
    }

    public static String getNome() {
        return Nome;
    }

    public void setNome(String nome) {
        Nome = nome;
    }

    public static String getToken() {
        return token;
    }

    public void setToken(String token) {
        this.token = token;
    }

    public List<String> getVagas() {
        return vagas;
    }

    public static String getVaga(int pos){
        return vagas.get(pos);
    }

    public void setVagas(List<String> vagas) {
        this.vagas = vagas;
    }
}
