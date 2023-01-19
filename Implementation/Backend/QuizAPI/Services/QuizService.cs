using QuizAPI.Core;
using VDS.RDF.Query;
using VDS.RDF.Parsing;
using System.Text.RegularExpressions;
using AngleSharp.Common;
using VDS.RDF.Writing.Formatting;

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

        public List<string> GetQueryAnswer(string querry, string character)
        {
            List<string> resultsList = new List<string>();  

            SparqlParameterizedString queryString = new SparqlParameterizedString();

            queryString.Namespaces.AddNamespace("foaf", new Uri("http://xmlns.com/foaf/0.1/"));
            queryString.Namespaces.AddNamespace("gada", new Uri("https://gada.cards.game.namespace.com/"));
            queryString.Namespaces.AddNamespace("poke", new Uri("https://triplydb.com/academy/pokemon/vocab/"));
            queryString.Namespaces.AddNamespace("rdfs", new Uri("http://www.w3.org/2000/01/rdf-schema#"));

            queryString.Namespaces.AddNamespace("dbo", new Uri("http://dbpedia.org/ontology/"));
            queryString.Namespaces.AddNamespace("geo", new Uri("http://www.opengis.net/ont/geosparql#"));
            queryString.Namespaces.AddNamespace("owl", new Uri("http://www.w3.org/2002/07/owl#"));
            queryString.Namespaces.AddNamespace("sdo", new Uri("https://schema.org/"));
            queryString.Namespaces.AddNamespace("ssn", new Uri("http://www.w3.org/ns/ssn/"));
            queryString.Namespaces.AddNamespace("swapi", new Uri("https://swapi.co/vocabulary/"));
            queryString.Namespaces.AddNamespace("xsd", new Uri("http://www.w3.org/2001/XMLSchema#"));
            queryString.Namespaces.AddNamespace("po", new Uri("http://purl.org/ontology/po/"));


            queryString.CommandText = querry;
            queryString.SetLiteral("value", character);

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

            //queryString.CommandText = "SELECT ?universeName WHERE {  " +
            //    "?character foaf:member ?universe;  rdfs:label \"" + characterName + "\". ?universe rdfs:label ?universeName.}";

            queryString.CommandText = "SELECT ?universeName WHERE {  " +
                "?character foaf:member ?universe;  rdfs:label @value. ?universe rdfs:label ?universeName.}";
            queryString.SetLiteral("value", characterName);

            SparqlQueryParser parser = new SparqlQueryParser();
            SparqlQuery query = parser.ParseFromString(queryString);

            SparqlRemoteEndpoint endpoint = new SparqlRemoteEndpoint(new Uri("http://localhost:3030/gada_set2/query"));
            SparqlResultSet results = endpoint.QueryWithResultSet(query.ToString());

            var result = results.First().ToString();
            var universe = result.Substring(result.IndexOf("=") + 1).Trim();

            return universe;
        }

        public QuestionToReturn GetRandomQuestion(List<string> characters)
        {

            int optionIndex = 1;
            int index = random.Next(characters.Count);
            var selectedCharacter = characters[index];

            var characterUniverse = GetCharacterUniverse(selectedCharacter);

            var questions = quiz.Questions.Where(q => q.QuestionType.ToLower().Equals(characterUniverse.ToLower())).ToList();

            index = random.Next(questions.Count);
            Question question = questions[index];
            var quizQuestion = String.Format(question.QuizQuestion, selectedCharacter);

            //var templateParts = Regex.Split("What colour is {0}?", 

            QuestionToReturn questionToReturn = new QuestionToReturn();
            questionToReturn.Question = quizQuestion;


            if(characterUniverse.ToLower().Equals("pokemon")) //DELETE IF IN THE FUTURE
            {
                var queryAnswer = GetQueryAnswer(question.Query, selectedCharacter);
                questionToReturn.Options = new Dictionary<string, List<string>>();
                questionToReturn.Options.Add("option" + (optionIndex++).ToString(), queryAnswer);

                var characterList = GetCharacters(characterUniverse);
                var character1 = characterList[random.Next(characters.Count)];
                queryAnswer = GetQueryAnswer(question.Query, character1);
                questionToReturn.Options.Add("option" + (optionIndex++).ToString(), queryAnswer);

                characterList.Remove(character1);
                var character2 = characterList[random.Next(characters.Count)];
                queryAnswer = GetQueryAnswer(question.Query, character2);
                questionToReturn.Options.Add("option" + optionIndex.ToString(), queryAnswer);

            }

            return questionToReturn;
        }

        private List<String> GetCharacters(string universe)
        {

            var characterList = new List<string>(); 

            SparqlParameterizedString queryString = new SparqlParameterizedString();

            queryString.Namespaces.AddNamespace("foaf", new Uri("http://xmlns.com/foaf/0.1/"));
            queryString.Namespaces.AddNamespace("rdfs", new Uri("http://www.w3.org/2000/01/rdf-schema#"));

            queryString.CommandText = "SELECT ?characterName " +
                "WHERE { ?pokemon foaf:member ?universe; rdfs:label ?characterName. ?universe rdfs:label @value.}";
            queryString.SetLiteral("value", universe);

            SparqlQueryParser parser = new SparqlQueryParser();
            SparqlQuery query = parser.ParseFromString(queryString);

            SparqlRemoteEndpoint endpoint = new SparqlRemoteEndpoint(new Uri("http://localhost:3030/gada_set2/query"));
            SparqlResultSet results = endpoint.QueryWithResultSet(query.ToString());

            characterList = results.Select(x => x[0].ToString()).ToList();  

            return characterList;
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
