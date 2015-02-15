using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;

namespace DataIncubator
{
    class Program
    {
        static void Main(string[] args)
        {
            var rawData = File.ReadLines(@"C:\Users\asvyatko\Desktop\hits.csv");
            //var rawData = File.ReadLines(@"C:\Users\asvyatko\Desktop\hits.small");


            var data = rawData.AsParallel().Select(l =>
            {
                var cells = l.Split(',');
                return new
                {
                    Date = DateTime.Parse(cells[0]),
                    UserId = int.Parse(cells[1]),
                    CatId = int.Parse(cells[2])
                };
            }).OrderBy(x => x.Date).ToList();


            var userGrops = data.GroupBy(x => x.UserId).ToList();

            //var timePairs = userGrops.SelectMany(g => g.Zip(g.Skip(1), (f, s) => (s.Date - f.Date).TotalSeconds)).ToList();
            //double average = timePairs.Average();
            //Console.WriteLine("Average: {0}", average);

            //var deltaCat = userGrops.SelectMany(g => g.Zip(g.Skip(1), (f, s) => s.CatId - f.CatId)).ToList();
            //double probab = (double)deltaCat.Count(x => x == 0) / deltaCat.Count;
            //Console.WriteLine("Same probab: {0}", probab);

            var catTransitions = new Dictionary<Tuple<int, int>, int>();

            var catTupels = userGrops.SelectMany(g => g.Zip(g.Skip(1), (f, s) => new Tuple<int, int>(f.CatId, s.CatId)))
                .Where(t => t.Item1 != t.Item2);

            foreach (var c in catTupels)
            {
                int count;
                if (catTransitions.TryGetValue(c, out count))
                {
                    catTransitions[c] += 1;
                }
                else
                {
                    catTransitions.Add(c, 1);
                }
            }

            int maxTrans = catTransitions.Max(x => x.Value);
            var maxTransKeys = catTransitions.Where(x => x.Value == maxTrans).First();
            int totalTrans = catTransitions.Sum(x => x.Value);

            Console.WriteLine("Max trans: {0} => {1} probab: {2}", maxTransKeys.Key.Item1, maxTransKeys.Key.Item2, (double)maxTrans / totalTrans);

        }
    }
}
