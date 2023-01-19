namespace QuizAPI.Core
{
    public class QuestionToReturn
    {
        public string Question { get; set; }

        public string QuestionType { get; set; }

        public string Subject { get; set; }

        public Dictionary<string, List<string>> Options { get; set; }   
    }
}
