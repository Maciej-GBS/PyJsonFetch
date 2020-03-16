from implementation import *
import unittest
from math import isnan
from io import StringIO

class TestGeoObject(unittest.TestCase):
    def test_radian(self):
        g = Geo(3.14, 2.8, False)
        self.assertAlmostEqual(g.lat, 3.14, 2)
        self.assertAlmostEqual(g.lon, 2.8, 2)
        self.assertAlmostEqual(g.lat_degree, 179.91, 2)
        self.assertAlmostEqual(g.lon_degree, 160.43, 2)
    
    def test_degree(self):
        g = Geo(352, -832)
        self.assertAlmostEqual(g.lat, 6.14, 2)
        self.assertAlmostEqual(g.lon, -14.52, 2)
        self.assertAlmostEqual(g.lat_degree, 352, 2)
        self.assertAlmostEqual(g.lon_degree, -832, 2)

    def test_distance(self):
        a = Geo(47.879917, 15.133688)
        b = Geo(54.091971, 32.184469)
        # Compared with Google Maps, acceptable error 1000m
        self.assertLess(abs(a.distance(b) - 1374180), 1000)

class TestMatrixSolver(unittest.TestCase):
    def test_solve(self):
        nan = float('nan')

        solver = MatrixSolver()
        solver.solve(list(range(1,4)))
        solution = [[nan,-1,-2],[1,nan,-1],[2,1,nan]]
        for i in range(0,len(solution)):
            for j in range(0,len(solution[i])):
                a = solver.matrix[i][j]
                b = solution[i][j]
                self.assertTrue(a == b or (isnan(a) and isnan(b)))

        solver = MatrixSolver((lambda x,y: x+y), True)
        solver.solve(list(range(1,4)))
        solution = [[nan,3,4],[3,nan,5],[4,5,nan]]
        for i in range(0,len(solution)):
            for j in range(0,len(solution[i])):
                a = solver.matrix[i][j]
                b = solution[i][j]
                self.assertTrue(a == b or (isnan(a) and isnan(b)))

    def test_minmax(self):
        solver = MatrixSolver()
        solver.solve(list(range(1,5)))
        self.assertListEqual(solver.min(), [3, 3, 3, 2])
        self.assertListEqual(solver.max(), [1, 0, 0, 0])

def test_data():
    posts = pd.read_csv(StringIO("""id,userId,title,body
    1,2,title other,reiciendis molestiae occaecati non minima eveniet qui voluptatibus ut animi commodi
    11,2,title duplicate,delectus reiciendis molestiae occaecati non minima eveniet qui voluptatibus ut animi commodi
    21,3,title duplicate,repellat aliquid praesentium dolorem quo""")).set_index(['id'])
    users = pd.read_csv(StringIO("""id,name,username,email,address,phone,website,company
    2,Ervin Howell,Antonette,Shanna@melissa.tv,\"{'street': 'Victor Plains', 'suite': 'Suite 879', 'city': 'Wisokyburgh', 'zipcode': '90566-7771', 'geo': {'lat': '-43.9509', 'lng': '-34.4618'}}\",010-692-6593 x09125,anastasia.net,\"{'name': 'Deckow-Crist', 'catchPhrase': 'Proactive didactic contingency', 'bs': 'synergize scalable supply-chains'}\"
    3,Clementine Bauch,Samantha,Nathan@yesenia.net,\"{'street': 'Douglas Extension', 'suite': 'Suite 847', 'city': 'McKenziehaven', 'zipcode': '59590-4157', 'geo': {'lat': '-68.6102', 'lng': '-47.0653'}}\",1-463-123-4447,ramiro.info,\"{'name': 'Romaguera-Jacobson', 'catchPhrase': 'Face to face bifurcated interface', 'bs': 'e-enable strategic applications'}\"""")).set_index(['id'])
    users.loc[:,'address'] = users.loc[:,'address'].apply(eval)
    return posts, users

class TestMain(unittest.TestCase):
    def test_fetch_error(self):
        with self.assertRaises(ValueError):
            fetch_json('http://')

    def test_make_df(self):
        df = make_dataframe([{'id':1, 'test':'test'}, {'id':2, 'test':'test'}])
        self.assertListEqual(list(df.columns), ['test'])
        self.assertListEqual(list(df.index), [1,2])

    def test_post_count(self):
        posts, users = test_data()
        answer = get_user_post_count(posts, users)
        solution = [f'{x} napisał(a) {y} postów' for x,y in [('Antonette',2), ('Samantha',1)]]
        self.assertListEqual(answer, solution)

    def test_duplicate_titles(self):
        posts, users = test_data()
        answer = get_duplicated_titles(posts)
        self.assertListEqual(['title duplicate'], answer)

    def test_nearest_users(self):
        posts, users = test_data()
        answer = get_nearest_users(users)
        self.assertDictEqual(answer, {2:3,3:2})

if __name__ == "__main__":
    unittest.main()
