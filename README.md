## Commit History

*   `feat: Add Item class with basic attributes`
    *   This commit introduces the `Item` class, which represents a library item. The class includes attributes for `item_id`, `title`, and `status`.

*   `feat: Implement borrow_item() method in LoanManager`
    *   This commit implements the `borrow_item()` method in the `LoanManager` class. This method allows borrowers to borrow items from the library.

*   `fix: Prevent borrowing an already borrowed item`
    *   This commit fixes a bug in the `borrow_item()` method that allowed borrowers to borrow items that were already borrowed.

*   `test: Add unit tests for Item class`
    *   This commit adds unit tests for the `Item` class to ensure that it is working correctly.

*   `docs: Update README with environment setup instructions`
    *   This commit updates the `README` file with instructions on how to set up the development environment for this project.

    * `feat: Implement Item, Borrower, and LoanManager classes`


*   **Branching:** New features and bug fixes are developed on separate branches.
*   **Merging:** Branches are merged back into the `main` branch after testing and code review.
*   **Commit Messages:** Commit messages are clear and concise, and they follow a consistent style.

Here's an example of creating a new branch, making changes, and merging the branch back into `main`:

1.  Create a new branch: `git checkout -b feature/add-logging`
2.  Make changes to the code.
3.  Commit the changes: `git add .`, `git commit -m "feat: Add logging to LoanManager"`
4.  Switch back to the `main` branch: `git checkout main`
5.  Merge the changes: `git merge feature/add-logging`
6.  Delete the branch: `git branch -d feature/add-logging`