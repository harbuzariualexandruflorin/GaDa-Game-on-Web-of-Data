using QuizAPI.Core;
using VDS.RDF.Query;

namespace QuizAPI.Services
{
    public interface IQuizService
    {
        string GetQueryOfQuestion(string question);

        List<string> GetQueryAnswer(string querry, string character);

        QuestionToReturn GetRandomQuestion(List<string> characters);

        bool CheckAnswer(Answer answer);
    }
}
