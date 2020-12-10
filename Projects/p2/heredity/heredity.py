import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    joint_prob = 1

    for person in people:
        
        # If person hasn't parents use PROBS for joint_prob update
        if people[person]["mother"] == None:
            
            # Update the joint_prob for 1 gene
            if person in one_gene:
                joint_prob *= PROBS['gene'][1]

                # Update the joint_prob for trait given 1 gene
                joint_prob = joint_prob_trait(person, have_trait, joint_prob, 1)
            
            # Update the joint_prob for 2 gene
            elif person in two_genes:
                joint_prob *= PROBS['gene'][2]

                # Update the joint_prob for trait given 2 gene
                joint_prob = joint_prob_trait(person, have_trait, joint_prob, 2)

            # Update the joint_prob for 0 gene
            else:
                joint_prob *= PROBS['gene'][0]

                # Update the joint_prob for trait given 0 gene
                joint_prob = joint_prob_trait(person, have_trait, joint_prob, 0)
        
        # If person has parents use parents PROBS for probability calculation
        else:
            
            # Update the joint_prob for 1 gene
            if person in one_gene:
                
                joint_prob *= p_child_genes(1, people[person]['mother'], people[person]['father'], one_gene, two_genes)

                # Update the joint_prob for trait given 1 gene
                joint_prob = joint_prob_trait(person, have_trait, joint_prob, 1)
            
            # Update the joint_prob for 2 gene
            elif person in two_genes:
                joint_prob *= p_child_genes(2, people[person]['mother'], people[person]['father'], one_gene, two_genes)

                # Update the joint_prob for trait given 2 gene
                joint_prob = joint_prob_trait(person, have_trait, joint_prob, 2)

            # Update the joint_prob for 0 gene
            else:
                joint_prob *= p_child_genes(0, people[person]['mother'], people[person]['father'], one_gene, two_genes)

                # Update the joint_prob for trait given 0 gene
                joint_prob = joint_prob_trait(person, have_trait, joint_prob, 0)

    return joint_prob


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person in have_trait:
            probabilities[person]['trait'][True] += p
        else:
            probabilities[person]['trait'][False] += p

        if person in one_gene:
            probabilities[person]['gene'][1] += p

        elif person in two_genes:
            probabilities[person]['gene'][2] += p
        
        else:
            probabilities[person]['gene'][0] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        
        sum_trait = (probabilities[person]['trait'][True]
                     + probabilities[person]['trait'][False])
        probabilities[person]['trait'][True] = probabilities[person]['trait'][True] / sum_trait
        probabilities[person]['trait'][False] = probabilities[person]['trait'][False] / sum_trait

        sum_gene = (probabilities[person]['gene'][0]
                    + probabilities[person]['gene'][1]
                    + probabilities[person]['gene'][2])
         
        probabilities[person]['gene'][0] = probabilities[person]['gene'][0] / sum_gene
        probabilities[person]['gene'][1] = probabilities[person]['gene'][1] / sum_gene
        probabilities[person]['gene'][2] = probabilities[person]['gene'][2] / sum_gene
    
    return probabilities


def joint_prob_trait(person, have_trait, joint_prob, n_gene):
    
    if person in have_trait:
        joint_p = PROBS['trait'][n_gene][True] * joint_prob
    else:
        joint_p = PROBS['trait'][n_gene][False] * joint_prob
    return joint_p


def p_pass(parent, one_gene, two_genes):
    """Calculates the probability of passing a gene, given the parants gene number"""
    if parent in two_genes:
        p = 1 * (1 - PROBS["mutation"])
    elif parent in one_gene:
        p = 0.5 * (1 - PROBS["mutation"]) + 0.5 * (PROBS["mutation"])
    else:
        p = PROBS["mutation"]
    return p


def p_child_genes(gene_number, mother, father, one_gene, two_genes):
    """Calculates the probability of passing gene_number of genes, given the parants gene number"""

    if gene_number == 0:
        return (1 - p_pass(mother, one_gene, two_genes))\
            * (1 - p_pass(father, one_gene, two_genes))

    if gene_number == 1:
        return p_pass(mother, one_gene, two_genes) * (1 - p_pass(father, one_gene, two_genes))\
            + p_pass(father, one_gene, two_genes) * (1 - p_pass(mother, one_gene, two_genes))

    if gene_number == 2:
        return p_pass(mother, one_gene, two_genes) * (p_pass(father, one_gene, two_genes))
    

if __name__ == "__main__":
    main()
