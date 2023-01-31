namespace QuizAPI.Core
{
    public class Question
    {
        public string QuizQuestion { get; set; }

        public string? QuestionType { get; set; }

        public string SparqlEndpointType { get; set; }  

        public bool MultipleChoice { get; set; }

        public string Query { get; set; }
    }
}
