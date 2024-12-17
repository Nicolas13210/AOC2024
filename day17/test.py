from solve import Computer

def run_test(iteration,c):
    print("Test",iteration)
    c.run()
    print(c)



def test_Computer():
    c = Computer([2,6],0,0,9)
    run_test(1,c)

    c = Computer([5,0,5,1,5,4],10,0,0)
    run_test(2,c)

    c = Computer([0,1,5,4,3,0],2024,0,0)
    run_test(3,c)

    c = Computer([1,7],0,29,0)
    run_test(4,c)
test_Computer()