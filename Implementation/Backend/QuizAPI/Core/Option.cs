namespace QuizAPI.Core
{
    public class Option
    {
        public string Value { get; set; }
        public bool Checked { get; set; }
        public bool? IsCorrect { get; set; } = false;
    }
}
