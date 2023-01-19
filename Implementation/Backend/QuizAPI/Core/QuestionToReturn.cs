namespace QuizAPI.Core
{
    public class QuestionToReturn
    {
        public string Question { get; set; }
        public Dictionary<string, List<string>> Options { get; set; }   
    }
}
