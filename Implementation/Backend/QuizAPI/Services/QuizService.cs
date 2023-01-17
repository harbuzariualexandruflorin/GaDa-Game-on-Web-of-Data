using QuizAPI.Core;
using VDS.RDF.Query;
using VDS.RDF.Parsing;

namespace QuizAPI.Services
{
    public class QuizService : IQuizService
    {
        private readonly Quiz quiz;
        static Random random = new Random();

        public QuizService(Quiz quiz)
        {
            this.quiz = quiz;
        }

        public List<string> GetQueryAnswer(string querry)
        {
            List<string> resultsList = new List<string>();  

            SparqlParameterizedString queryString = new SparqlParameterizedString();

            queryString.Namespaces.AddNamespace("foaf", new Uri("http://xmlns.com/foaf/0.1/"));
            queryString.Namespaces.AddNamespace("gada", new Uri("https://gada.cards.game.namespace.com/"));
            queryString.Namespaces.AddNamespace("poke", new Uri("https://triplydb.com/academy/pokemon/vocab/"));
            queryString.Namespaces.AddNamespace("rdfs", new Uri("http://www.w3.org/2000/01/rdf-schema#"));

            queryString.CommandText = querry;

            SparqlQueryParser parser = new SparqlQueryParser();
            SparqlQuery query = parser.ParseFromString(queryString);

            SparqlRemoteEndpoint endpoint = new SparqlRemoteEndpoint(new Uri("http://localhost:3030/gada_set2/query"));
            SparqlResultSet results = endpoint.QueryWithResultSet(query.ToString());
          
            
            foreach (SparqlResult result in results)
            {
                resultsList.Add(result.ToString());
                Console.WriteLine(result.ToString());
            }
            return resultsList;
        }

        public string GetQueryOfQuestion(string question)
        {
            return quiz.Questions.Find(q => q.QuizQuestion.Equals(question)).Query;
        }

        private string GetCharacterUniverse(string characterName)
        {
            SparqlParameterizedString queryString = new SparqlParameterizedString();
            queryString.Namespaces.AddNamespace("foaf", new Uri("http://xmlns.com/foaf/0.1/"));
            queryString.Namespaces.AddNamespace("rdfs", new Uri("http://www.w3.org/2000/01/rdf-schema#"));

            queryString.CommandText = "SELECT ?universeName WHERE {  " +
                "?character foaf:member ?universe;  rdfs:label \"" + characterName + "\". ?universe rdfs:label ?universeName.}";

            SparqlQueryParser parser = new SparqlQueryParser();
            SparqlQuery query = parser.ParseFromString(queryString);

            SparqlRemoteEndpoint endpoint = new SparqlRemoteEndpoint(new Uri("http://localhost:3030/gada_set2/query"));
            SparqlResultSet results = endpoint.QueryWithResultSet(query.ToString());

            var result = results.First().ToString();
            var universe = result.Substring(result.IndexOf("=") + 1).Trim().ToLower();

            return universe;
        }

        public string GetRandomQuestion(List<string> characters)
        {
            int index = random.Next(characters.Count);
            var selectedCharacter = characters[index];
            Console.WriteLine("SELECTED CHARACTER: " + selectedCharacter);

            var characterUniverse = GetCharacterUniverse(selectedCharacter);

            var questions = quiz.Questions.Where(q => q.QuestionType.ToLower().Equals(characterUniverse)).ToList();

            index = random.Next(questions.Count);
            var questionToReturn = questions[index].QuizQuestion;

            return questionToReturn;
        }

        /*
        public string GetRandomQuestion(string topic)
        {
            SparqlParameterizedString queryString = new SparqlParameterizedString();

            queryString.Namespaces.AddNamespace("foaf", new Uri("http://xmlns.com/foaf/0.1/"));
            queryString.Namespaces.AddNamespace("gada", new Uri("https://gada.cards.game.namespace.com/"));
            queryString.Namespaces.AddNamespace("rdfs", new Uri("http://www.w3.org/2000/01/rdf-schema#"));

            queryString.CommandText = "SELECT ?pokemonName WHERE { " +
                "?pokemon foaf:member gada:univ_Pokemon; rdfs:label ?pokemonName.}";

            SparqlQueryParser parser = new SparqlQueryParser();
            SparqlQuery query = parser.ParseFromString(queryString);

            SparqlRemoteEndpoint endpoint = new SparqlRemoteEndpoint(new Uri("http://localhost:3030/gada_set2/query"));
            SparqlResultSet results = endpoint.QueryWithResultSet(query.ToString());

            int index = random.Next(results.Count);
            string characterName = results.GetItemByIndex(index).ToString();

            return characterName;
        }
        */
    }
}
