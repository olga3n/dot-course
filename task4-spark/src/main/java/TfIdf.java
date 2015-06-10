
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.SparkConf;

import org.apache.spark.api.java.JavaPairRDD;
import scala.Tuple2;
import org.apache.spark.api.java.function.Function;
import org.apache.spark.api.java.function.FlatMapFunction;
import org.apache.spark.api.java.function.Function2;
import org.apache.spark.api.java.function.PairFunction;

import java.util.Arrays;
import java.util.List;
import java.util.ArrayList;
import java.util.regex.Pattern;
import java.util.Map;
import java.util.HashMap;
import java.util.Iterator;
import java.lang.Math;

import java.io.File;

public final class TfIdf {

	private static final Pattern SPACE = Pattern.compile("\\s+");

	public static void main(String[] args) throws Exception {
		
		if (args.length < 2) {
			System.err.println("Usage: TfIdf <corpus> <text>");
			System.exit(1);
		}
		
		SparkConf conf = new SparkConf().setAppName("TfIdf");
		JavaSparkContext ctx = new JavaSparkContext(conf);

		// TF --------------------------------------------------------

		JavaRDD<String> lines = ctx.textFile(args[1], 1);

		JavaRDD<String> words = lines.flatMap(
			new FlatMapFunction<String, String>() {
				
				@Override
				public Iterable<String> call(String s) {
					return Arrays.asList(SPACE.split(s));
				}
			});

		JavaPairRDD<String, Integer> ones = words.mapToPair(
			new PairFunction<String, String, Integer>() {
				
				@Override
				public Tuple2<String, Integer> call(String s) {
					return new Tuple2<String, Integer>(s, 1);
				}
			});

		JavaPairRDD<String, Integer> counts = ones.reduceByKey(
			new Function2<Integer, Integer, Integer>() {
				@Override
				public Integer call(Integer i1, Integer i2) {
					return i1 + i2;
				}
			});

		final Long count = ones.count();

		JavaPairRDD<String, Double> tf = counts.mapToPair(
			new PairFunction<Tuple2<String, Integer>, String, Double>() {
				
				@Override
				public Tuple2<String, Double> call(Tuple2<String, Integer> item) 
					throws Exception 
				{
					return new Tuple2<String, Double>(
						item._1(), (double)item._2() / (double)count );
				}
			});

		// IDF ----------------------------------------------------

		String path = args[0];
		File[] listOfFiles = new File(path).listFiles();

		final int N = listOfFiles.length;

		Map<String, Object> map = new HashMap<String, Object>();

		for (File file : listOfFiles) {
			JavaRDD<String> fileLines = ctx.textFile(
					path + "/" + file.getName(), 1
				);

			JavaRDD<String> fileWords = fileLines.flatMap(
				new FlatMapFunction<String, String>() {
				
					@Override
					public Iterable<String> call(String s) {
						return Arrays.asList(SPACE.split(s));
					}
				});

			JavaPairRDD<String, Integer> fileOnes = fileWords.mapToPair(
				new PairFunction<String, String, Integer>() {
				
					@Override
					public Tuple2<String, Integer> call(String s) {
						return new Tuple2<String, Integer>(s, 1);
					}
				});

			JavaPairRDD<String, Tuple2<Integer, Integer>> file_group = 
				counts.join(fileOnes.distinct());

			final Map<String, Object> df_part = file_group.countByKey();

			for (Iterator<String> iterator = df_part.keySet().iterator(); 
					iterator.hasNext();) 
			{
				String key = (String) iterator.next();
				Object value = 1;

				if(map.containsKey(key)){
					value = (1 + new Integer( map.get(key).toString() ) );
				}

				map.put(key, value);
			}			
		}

		final Map<String, Object> df = map;

		System.out.println(df.toString());
		
		// TF-IDF -----------------------------------------

		JavaPairRDD<String, Double> tfidf = tf.mapToPair(
			new PairFunction<Tuple2<String, Double>, String, Double>() {
				
				@Override
				public Tuple2<String, Double> call(Tuple2<String, Double> item) 
					throws Exception 
				{
					return new Tuple2<String, Double>(
						item._1(), item._2() * 
						Math.log( (double) N / new Integer(
							df.get(item._1()).toString() ) )
					);
				}
			});;

		JavaPairRDD<Double, String> swapped = tfidf.mapToPair(
			new PairFunction<Tuple2<String, Double>, Double, String>() {
				
				@Override
				public Tuple2<Double, String> call(Tuple2<String, Double> item) 
					throws Exception 
				{
					return item.swap();
				}
			});

		List<Tuple2<Double, String>> output = swapped.sortByKey(false).take(15);

		for (Tuple2<Double, String> tuple : output) {
			System.out.format("%s %f\n", tuple._2(), tuple._1());
		}

		ctx.stop();
	}

}