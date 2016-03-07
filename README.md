# sequence_totalisator

Haşim Sak'ın Analyzer sonuçlarının, istatistiksel bilgilerini çıkartan bir program.

Python3.4 ile yazılmıştır.


HOW TO RUN:
-----------
> python3.4 morphological_analyzer_totalisator.py test.txt


INPUT --> Haşim Sak analyzer kodunun vermiş olduğu çıktı programa input olarak verilmelidir.
	  --> örnek dosya içeriği:
		    <S> <S>+BSTag
			Bu bu[Pron]+[Demons]+[A3sg]+[Pnon]+[Nom] bu[Adj] bu[Det]
			hakkı Hak[Noun]+[A3sg]+SH[P3sg]+[Nom] Hak[Noun]+[A3sg]+[Pnon]+YH[Acc] hak(I)[Noun]+[A3sg]+SH[P3sg]+[Nom] hak(I)[Noun]+[A3sg]+[Pnon]+YH[Acc] Hakkı[Noun]+[Prop]+[A3sg]+[Pnon]+[Nom] hak[Adj]-[Noun]+[A3sg]+SH[P3sg]+[Nom] hak[Adj]-[Noun]+[A3sg]+[Pnon]+YH[Acc]
			yiyenler ye[Verb]+[Pos]-YAn[Adj+PresPart]-[Noun]+lAr[A3pl]+[Pnon]+[Nom]
			başta baş[Noun]+[A3sg]+[Pnon]+DA[Loc] başta[Adv] başta[Adj]
			hakemlerdir. hakemlerdir.[Unknown]
			</S> </S>+ESTag
			<S> <S>+BSTag
			Kayserispor Kayserispor[Noun]+[Prop]+[A3sg]+[Pnon]+[Nom]
			maçına maç[Noun]+[A3sg]+SH[P3sg]+NA[Dat] maç[Noun]+[A3sg]+Hn[P2sg]+NA[Dat]
			iyi iyi[Adv] iyi[Adj] iyi[Noun]+[A3sg]+[Pnon]+[Nom]
			başladık, başladık,[Unknown]
			iyi iyi[Adv] iyi[Adj] iyi[Noun]+[A3sg]+[Pnon]+[Nom]
			de de[Noun]+[A3sg]+[Pnon]+[Nom] de[Conj] de[Verb]+[Pos]+[Imp]+[A2sg]
			mücadele mücadele[Noun]+[A3sg]+[Pnon]+[Nom]
			ettik. ettik.[Unknown]
			</S> </S>+ESTag

OUTPUT -->	"sorted_parsing_statistic.mc" isimli bir dosya çıktı olarak verilir.
	   --> örnek dosya içeriği:
	   		  Parse_Number    	  Total        Ratio    		 Random_Guess           Random_Guess_Accuracy
			             1  	4830283  	   0.498826          1                      0.498826
			            10  	  10863  	   0.00112183        0.1                    0.000112183
			            11  	   1421  	   0.000146748       0.0909091              1.33407e-05
			            12  	  20925  	   0.00216094        0.0833333              0.000180078
			            13  	    392  	   4.04821e-05       0.0769231              3.11401e-06
			            14  	   1051  	   0.000108537       0.0714286              7.75267e-06
			            15  	    470  	   4.85372e-05       0.0666667              3.23581e-06
			            16  	   5830  	   0.000602068       0.0625                 3.76292e-05
			            17  	     13  	   1.34252e-06       0.0588235              7.89717e-08
			            18  	    187  	   1.93116e-05       0.0555556              1.07287e-06
			            19  	      2  	   2.06541e-07       0.0526316              1.08706e-08
			             2  	1919322  	   0.19821           0.5                    0.0991048
			            20  	   1343  	   0.000138692       0.05                   6.93462e-06
			            21  	      3  	   3.09812e-07       0.047619               1.47529e-08
			            22  	      3  	   3.09812e-07       0.0454545              1.40824e-08
			            24  	     75  	   7.7453e-06        0.0416667              3.22721e-07
			            27  	      1  	   1.03271e-07       0.037037               3.82484e-09
			            28  	    173  	   1.78658e-05       0.0357143              6.38065e-07
			             3  	1087687  	   0.112326          0.333333               0.037442
			            32  	     11  	   1.13598e-06       0.03125                3.54993e-08
			            36  	      2  	   2.06541e-07       0.0277778              5.73726e-09
			             4  	1007169  	   0.104011          0.25                   0.0260027
			             5  	 350208  	   0.0361662         0.2                    0.00723324
			             6  	 169024  	   0.0174552         0.166667               0.0029092
			             7  	 127030  	   0.0131185         0.142857               0.00187407
			             8  	 136047  	   0.0140497         0.125                  0.00175621
			             9  	  13760  	   0.001421          0.111111               0.000157889

	   --> parse_number 		: çözümleme sayısını göstermektedir.
	   	   Total       			: verilen parse_number sayısında kaç tane kelime olduğunu göstermektedir. 
	   	   Ratio       			: verilen parse_number sayısına sahip kelimelerin toplam corpusun yüzde kaçını oluşturduğunu göstermektedir.
	   	   Random_Guess 		: verilen parse_number için rastgele bir çözüm seçildiğinde doğru tahmin etme ihtimalini göstermektedir.
	   	   Random_Guess_Accuracy: verilen parse_number için rastgele bir çözüm seçildiğinde, doğru tahmin edilirse corpusun kaçlık kısmı doğru tespit edilmiş oluyor.

	   	   Ör: parse_number = 1 olduğu durum için, yani tek bir çözümlemesi olan kelimeler için.
	   	       Total = 4830283, yani bu kadar kelimenin bir tane çözümlemesi var  
	   	       Ratio = 49%, yani toplam corpusun yüzde 49 tek çözümlü kelimelerden oluşmaktadır.
	   	       Random_Guess =  1, yani rastgele bir çözüm seçildiğinde doğru olanı tespit etme yüzdesini gösterir. Tek çözüm için 100% doğru tespit edilir.