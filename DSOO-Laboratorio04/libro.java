class libro{
    private String titulo;
    private String autor;
    private String ISBN;
    private boolean disponible;

    public Libro() { 
        this.titulo = "Sin título";
        this.autor = "Desconocido";
        this.ISBN = "0000";
        this.disponible = true;
    }

    public Libro(String titulo, String autor, String ISBN, boolean disponible) {
        this.titulo = titulo;
        this.autor = autor;
        this.ISBN = ISBN;
        this.disponible = disponible;
    }

    public String getTitulo() { return titulo; }
    public void setTitulo(String titulo) { this.titulo = titulo; }

    public String getAutor() { return autor; }
    public void setAutor(String autor) { this.autor = autor; }

    public String getISBN() { return ISBN; }
    public void setISBN(String ISBN) { this.ISBN = ISBN; }

    public boolean isDisponible() { return disponible; }
    public void setDisponible(boolean disponible) { this.disponible = disponible; }

    public boolean estaDisponible() {
        return disponible;
    }
    @Override
    public String toString() {
        return "Título: " + titulo +", Autor: " + autor + ", ISBN: " + ISBN + ", Disponible: " + (disponible ? "Sí" : "No");
    }

}
    
