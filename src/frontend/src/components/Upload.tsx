import React, { useState } from "react";

const FileUpload: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState<string>("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (file) {
      const formData = new FormData();
      formData.append("file", file);
      // Removido o id_modelo
      // formData.append("id_modelo", "1"); 

      try {
        const response = await fetch("http://100.29.57.65:8001/retrain", {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          const data = await response.json();
          console.log("Resposta do servidor:", data);
          setMessage(`Arquivo "${file.name}" foi enviado com sucesso!`);
        } else {
          // Tentar obter a mensagem de erro
          let errorMessage = '';
          try {
            const errorData = await response.json();
            console.error("Erro ao enviar o arquivo:", errorData);
            // Verificar se errorData.detail é uma string ou objeto
            if (typeof errorData.detail === 'string') {
              errorMessage = errorData.detail;
            } else if (Array.isArray(errorData.detail)) {
              // Caso o detalhe seja uma lista de erros
              errorMessage = errorData.detail.join(', ');
            } else {
              errorMessage = JSON.stringify(errorData.detail);
            }
          } catch (parseError) {
            // Caso a resposta não seja um JSON válido
            errorMessage = await response.text();
            console.error("Erro ao parsear a resposta de erro:", parseError);
          }
          setMessage(`Erro ao enviar o arquivo: ${errorMessage}`);
        }
      } catch (error) {
        console.error("Erro na requisição:", error);
        setMessage("Erro ao enviar o arquivo. Por favor, tente novamente.");
      }
    } else {
      setMessage("Por favor, selecione um arquivo antes de enviar.");
    }
  };

  return (
    <div className="min-h-screen bg-white flex items-center justify-center">
      <div className="bg-white shadow-md rounded-lg p-8 w-full max-w-md border border-gray-200">
        <h2 className="text-2xl font-semibold text-center mb-6 text-[#2f94bf]">Upload de Arquivo</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="mb-4">
            <label className="block text-gray-700 font-medium mb-2">Selecione um arquivo:</label>
            <input
              type="file"
              accept=".csv, .xlsx"
              onChange={handleFileChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-[#2f94bf] focus:border-[#2f94bf] focus:outline-none"
            />
          </div>
          {message && (
            <p className={`text-center ${file ? "text-green-500" : "text-red-500"} font-medium`}>
              {message}
            </p>
          )}
          <button
            type="submit"
            className="w-full bg-[#2f94bf] text-white font-semibold py-2 px-4 rounded-lg hover:bg-[#237b99] focus:outline-none focus:ring-2 focus:ring-[#2f94bf] focus:ring-opacity-50"
          >
            Enviar Arquivo
          </button>
        </form>
      </div>
    </div>
  );
};

export default FileUpload;