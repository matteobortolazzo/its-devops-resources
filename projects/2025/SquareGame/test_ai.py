#!/usr/bin/env python3
"""
Simple test to verify the AI system works
"""
from ai_player import NeuroEvolution, AIAgent, DodgeNet
import torch

def test_neural_network():
    """Test that the neural network can be created and used"""
    print("Testing Neural Network...")
    net = DodgeNet()

    # Test forward pass
    test_state = [0.5, 0.0, 0.3, 0.2, -0.2, 0.6, 0.4, 0.1]
    action = net.get_action(test_state)
    print(f"  Network created ✓")
    print(f"  Forward pass works ✓")
    print(f"  Sample action: {action} (0=left, 1=stay, 2=right)")

def test_agent():
    """Test that agents can be created, cloned, and mutated"""
    print("\nTesting AI Agent...")
    agent1 = AIAgent()
    print(f"  Agent created ✓")

    agent2 = agent1.clone()
    print(f"  Agent cloned ✓")

    agent2.mutate()
    print(f"  Agent mutated ✓")

    # Test that they give different actions after mutation
    test_state = [0.5, 0.0, 0.3, 0.2, -0.2, 0.6, 0.4, 0.1]
    action1 = agent1.get_action(test_state)
    action2 = agent2.get_action(test_state)
    print(f"  Original agent action: {action1}")
    print(f"  Mutated agent action: {action2}")

def test_evolution():
    """Test that evolution system works"""
    print("\nTesting Neuroevolution...")
    evo = NeuroEvolution(population_size=10, elite_size=3)
    print(f"  Population created: {len(evo.population)} agents ✓")

    # Set some fitness values
    for i, agent in enumerate(evo.population):
        agent.fitness = i * 10

    evo.evolve()
    print(f"  Evolution step completed ✓")
    print(f"  Generation: {evo.generation}")
    print(f"  Best fitness: {evo.best_fitness}")

def test_save_load():
    """Test saving and loading agents"""
    print("\nTesting Save/Load...")
    agent = AIAgent()

    # Save
    torch.save(agent.network.state_dict(), "test_agent.pth")
    print(f"  Agent saved ✓")

    # Load
    loaded_net = DodgeNet()
    loaded_net.load_state_dict(torch.load("test_agent.pth"))
    loaded_agent = AIAgent(loaded_net)
    print(f"  Agent loaded ✓")

    # Verify they produce same actions
    test_state = [0.5, 0.0, 0.3, 0.2, -0.2, 0.6, 0.4, 0.1]
    action1 = agent.get_action(test_state)
    action2 = loaded_agent.get_action(test_state)
    assert action1 == action2, "Loaded agent should produce same action"
    print(f"  Actions match: {action1} == {action2} ✓")

    # Cleanup
    import os
    os.remove("test_agent.pth")
    print(f"  Cleanup done ✓")

if __name__ == "__main__":
    print("=" * 50)
    print("AI System Tests")
    print("=" * 50)

    try:
        test_neural_network()
        test_agent()
        test_evolution()
        test_save_load()

        print("\n" + "=" * 50)
        print("✓ All tests passed!")
        print("=" * 50)
        print("\nYou can now:")
        print("  1. Train the AI: python train_ai.py")
        print("  2. Watch AI play: python demo_ai.py")
        print("  3. Play yourself: python main.py")

    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

