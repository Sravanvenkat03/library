import http from 'k6/http';
import { check, sleep } from 'k6';
import { randomIntBetween } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';

const baseUrl = 'http://localhost:8000';

export const options = {
  stages: [
    { duration: '15s', target: 10 },  // Ramp up to 20 users
    { duration: '10', target: 10 },    // Stay at 20 users
    { duration: '15s', target: 0 },     // Ramp down to 0 users
  ],
};

export default function () {
  const bookId = randomIntBetween(1000, 10000);
  const bookPayload = JSON.stringify([{
    id: bookId,
    title: `Book Title ${bookId}`,
    author: 'Author Name',
    year: 2021,
    isbn: `ISBN-${bookId}`,
  }]);

  // Add a book
  const addBookRes = http.post(`${baseUrl}/books/`, bookPayload, {
    headers: { 'Content-Type': 'application/json' },
  });
  check(addBookRes, {
    'added book successfully': (res) => res.status === 200,
  });
  if (addBookRes.status !== 200) {
    console.log(`Failed to add book: ${addBookRes.body}`);
  }

  // Retrieve the book
  const getbook= JSON.stringify([bookId]);
  const getBookRes = http.del(`${baseUrl}/books/`, getbook, {
    headers: { 'Content-Type': 'application/json' },
  });
  check(getBookRes, {
    'retrieved book successfully': (res) => res.status === 200,
  });
  if (getBookRes.status !== 200) {
    console.log(`Failed to retrieve book: ${getBookRes.body}`);
  }

  // Update the book
  const updateBookPayload = JSON.stringify([{
    id: bookId,
    title: `Updated Book Title ${bookId}`,
    author: 'Updated Author Name',
  }]);
  const updateBookRes = http.put(`${baseUrl}/books/`, updateBookPayload, {
    headers: { 'Content-Type': 'application/json' },
  });
  check(updateBookRes, {
    'updated book successfully': (res) => res.status === 200,
  });
  if (updateBookRes.status !== 200) {
    console.log(`Failed to update book: ${updateBookRes.body}`);
  }

  // Delete the book
  const deleteBookPayload = JSON.stringify([bookId]);
  const deleteBookRes = http.del(`${baseUrl}/books/`, deleteBookPayload, {
    headers: { 'Content-Type': 'application/json' },
  });
  check(deleteBookRes, {
    'deleted book successfully': (res) => res.status === 200,
  });
  if (deleteBookRes.status !== 200) {
    console.log(`Failed to delete book: ${deleteBookRes.body}`);
  }

  // User ID for testing
  const userId = randomIntBetween(1000, 10000);
  const userPayload = JSON.stringify([{
    id: userId,
    name: `User Name ${userId}`,
    email: `user${userId}@example.com`,
  }]);

  // Add a user
  const addUserRes = http.post(`${baseUrl}/users/`, userPayload, {
    headers: { 'Content-Type': 'application/json' },
  });
  check(addUserRes, {
    'added user successfully': (res) => res.status === 200,
  });
  if (addUserRes.status !== 200) {
    console.log(`Failed to add user: ${addUserRes.body}`);
  }

  // Delete the user
  const deleteUserPayload = JSON.stringify([userId]);
  const deleteUserRes = http.del(`${baseUrl}/users/`, deleteUserPayload, {
    headers: { 'Content-Type': 'application/json' },
  });
  check(deleteUserRes, {
    'deleted user successfully': (res) => res.status === 200,
  });
  if (deleteUserRes.status !== 200) {
    console.log(`Failed to delete user: ${deleteUserRes.body}`);
  }

  sleep(1);  // Sleep for 1 second before the next iteration
}
