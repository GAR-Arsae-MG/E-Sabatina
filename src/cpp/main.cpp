#include <iostream>
#include <pybind11/embed.h>
#include <pybind11/stl.h>
#include <vector>

namespace py = pybind11;

int main() {
  // Start interpreter
  py::scoped_interpreter guard{};

  try {
    // Add your project directory to PYTHONPATH
    py::module sys = py::module::import("sys");
    sys.attr("path").cast<py::list>().append("../src/python/services");

    // Import your class
    py::module serviceMod = py::module::import("BERTimbauService");
    py::object cls = serviceMod.attr("BERTimbauService");

    // Instantiate
    py::object service = cls();

    std::string sentence = "A multa será de 10% em caso de atraso.";

    // Call get_sentence_embedding
    py::object result = service.attr("get_sentence_embedding")(sentence);

    std::vector<float> vec = result.cast<std::vector<float>>();

    std::cout << "Embedding dim: " << vec.size() << "\n";
    std::cout << "First 5 values: ";
    for (int i = 0; i < 5; i++) {
      std::cout << vec[i] << " ";
    }
    std::cout << "\n";

    // Token embeddings
    py::object tokres = service.attr("get_token_embeddings")(sentence);
    py::dict d = tokres.cast<py::dict>();
    std::cout << "Token count: " << py::len(d["tokens"]) << "\n";

  } catch (const py::error_already_set &e) {
    std::cerr << "Python error: " << e.what() << "\n";
  }

  return 0;
}
